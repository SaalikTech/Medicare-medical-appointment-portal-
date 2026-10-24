import os
from pathlib import Path
from extensions import db
from models import Booking 
import psycopg
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def create_users_table():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    password_hash TEXT NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'patient'
                        CHECK (role IN ('patient', 'admin')),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)

            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS
                users_email_lower_unique
                ON users (LOWER(email));
            """)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_user(email, password, role="patient"):
    email = email.strip().lower()

    if not email or len(email) > 255:
        raise ValueError("Please provide a valid email address.")

    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters.")

    if role not in ("patient", "admin"):
        raise ValueError("Invalid account role.")

    # Hash the password before storing it.
    password_hash = generate_password_hash(password)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (email, password_hash, role)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (email, password_hash, role)
            )

            user_id = cursor.fetchone()[0]

        conn.commit()
        return user_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def add_booking(user_name, email, dr, date, time, patient_id=None):
    if is_conflict(dr, date, time):
        return False

    booking = Booking(
        user_name=user_name,
        email=email,
        dr=dr,
        date=date,
        time=time,
        status="Confirmed",
        patient_id=patient_id,
    )

    db.session.add(booking)
    db.session.commit()
    return True

def is_conflict(dr, date, time):
    conflict = db.session.execute(
        db.select(Booking.id).where(
            Booking.dr == dr,
            Booking.date == date,
            Booking.time == time,
        ).limit(1)
    ).first()

    return conflict is not None