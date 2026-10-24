from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=True)
    user_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    dr = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default="Confirmed")



class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
    )

    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.Text, nullable=True)
    blood_type = db.Column(db.String(3), nullable=True)
    gp_name = db.Column(db.String(150), nullable=True)
    gp_contact = db.Column(db.String(50), nullable=True)


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    speciality = db.Column(db.String(150), nullable=False)
    qualifications = db.Column(db.String(250), nullable=True)
    biography = db.Column(db.Text, nullable=True)

    hospital = db.Column(db.String(200), nullable=True)
    station = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(150), nullable=True)

    salary = db.Column(db.Numeric(10, 2), nullable=True)
    availability = db.Column(db.String(250), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )
