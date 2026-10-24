import os
from dotenv import load_dotenv

load_dotenv()

# Keep automated tests separate from the main database.
os.environ["DB_NAME"] = "medical_portal_test"

from app import app
from extensions import db
from database import add_booking, is_conflict
from models import Booking, User as UserModel, Patient

def test_homepage_loads():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.location



# def test_homepage_loads():
#     app.config["TESTING"] = True
#     client = app.test_client()

#     response = client.get("/")

#     assert response.status_code == 200


def test_login_page_loads():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/login", follow_redirects=False)

    print("Login status:", response.status_code)
    print("Login redirect:", response.location)

    assert response.status_code == 200

    
# def test_login_page_loads():
#     app.config["TESTING"] = True

#     client = app.test_client()
#     login_test_patient(client)
#     response = client.get("/login")

#     assert response.status_code == 200


def test_admin_requires_login():
    app.config["TESTING"] = True
    client = app.test_client()

    with client.session_transaction() as session:
        session.clear()

    response = client.get("/admin", follow_redirects=False)

    print("Status:", response.status_code)
    print("Redirect:", response.location)

    assert response.status_code == 302
    assert "/login" in response.location

def test_patient_cannot_access_admin():
    app.config["TESTING"] = True

    with app.app_context():
        patient = UserModel.query.filter_by(role="patient").first()

        assert patient is not None, "Create a demo patient account first."
        patient_id = str(patient.id)

    client = app.test_client()
    login_test_patient(client)

    with client.session_transaction() as session:
        session["_user_id"] = patient_id
        session["_fresh"] = True

    response = client.get("/admin")

    assert response.status_code == 403



def login_test_patient(client):
    with app.app_context():
        patient = db.session.execute(
            db.select(UserModel).where(
                UserModel.role == "patient"
            )
        ).scalar_one()

        patient_id = str(patient.id)

        # Ensure this test user has a patient profile.
        profile = db.session.execute(
            db.select(Patient).where(
                Patient.user_id == patient.id
            )
        ).scalar_one_or_none()

        if profile is None:
            profile = Patient(
                user_id=patient.id,
                full_name="Test Patient",
                email=patient.email,
            )
            db.session.add(profile)
            db.session.commit()

    with client.session_transaction() as session:
        session["_user_id"] = patient_id
        session["_fresh"] = True

def test_booking_missing_fields():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()
    login_test_patient(client)

    response = client.post(
        "/book",
        data={},
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.location.endswith("/")


def test_successful_booking(monkeypatch):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    monkeypatch.setattr("app.add_booking",lambda *args, **kwargs: True)


    client = app.test_client()
    login_test_patient(client)

    response = client.post(
        "/book",
        data={
            "user_name": "Test Patient",
            "email": "test@example.com",
            "dr": "Dr Test",
            "date": "2026-11-10",
            "time": "10:00"
        },
        follow_redirects=False
    )

    print("Status:", response.status_code)
    print("Redirect location:", response.location)
    assert response.status_code == 302
    
    assert response.status_code == 302
    assert response.location.endswith("/")


def test_booking_conflict(monkeypatch):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Simulate a booking conflict
    monkeypatch.setattr("app.add_booking",lambda *args, **kwargs: False)

    client = app.test_client()
    login_test_patient(client)

    response = client.post(
        "/book",
        data={
            "user_name": "Test Patient",
            "email": "test@example.com",
            "dr": "Dr Test",
            "date": "2026-11-10",
            "time": "10:00",
        },
        follow_redirects=False,
    )

       
    assert response.status_code == 302
    assert response.location.endswith("/")


with app.app_context():
    db.create_all()

    patient = db.session.execute(
        db.select(UserModel).where(
            UserModel.role == "patient"
        )
    ).scalar_one_or_none()

    if patient is None:
        test_patient = UserModel(
            email="pytest-patient@example.com",
            password_hash="test-only-placeholder",
            role="patient",
        )
        db.session.add(test_patient)
        db.session.commit()


    admin = db.session.execute(
        db.select(UserModel).where(
            UserModel.role == "admin"
        )
    ).scalar_one_or_none()

    if admin is None:
        test_admin = UserModel(
            email="pytest-admin@example.com",
            password_hash="test-only-placeholder",
            role="admin",
        )
        db.session.add(test_admin)
        db.session.commit()


def test_database_booking_and_conflict():
    with app.app_context():
        doctor = "Dr Pytest Integration"
        date = "2099-01-01"
        time = "09:17"

        # Remove any leftover test record before starting.
        db.session.query(Booking).filter_by(
            dr=doctor, date=date, time=time
        ).delete()
        db.session.commit()

        try:
            # The first appointment should be saved.
            assert add_booking(
                "Pytest Patient",
                "pytest@example.com",
                doctor,
                date,
                time,
            ) is True

            # PostgreSQL should now report a conflict.
            assert is_conflict(doctor, date, time) is True

            # The same slot should be rejected.
            assert add_booking(
                "Another Test Patient",
                "another-pytest@example.com",
                doctor,
                date,
                time,
            ) is False

        finally:
            # Remove only this test's appointment.
            db.session.query(Booking).filter_by(
                dr=doctor, date=date, time=time
            ).delete()
            db.session.commit()



def login_test_admin(client):
    with app.app_context():
        admin = db.session.execute(
            db.select(UserModel).where(
                UserModel.role == "admin"
            )
        ).scalar_one()

        admin_id = str(admin.id)

    with client.session_transaction() as session:
        session["_user_id"] = admin_id
        session["_fresh"] = True


def test_admin_can_view_appointments():
    app.config["TESTING"] = True
    client = app.test_client()
    login_test_admin(client)

    response = client.get("/admin")

    assert response.status_code == 200


def test_admin_can_export_appointments():
    app.config["TESTING"] = True
    client = app.test_client()
    login_test_admin(client)

    response = client.get("/export_json")

    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json(), list)
