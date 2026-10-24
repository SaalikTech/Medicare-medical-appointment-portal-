
from database import get_connection


def seed_data():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # Insert a fictional test patient
            cursor.execute(
                """
                INSERT INTO patients (full_name, email)
                VALUES (%s, %s)
                ON CONFLICT (email)
                DO UPDATE SET full_name = EXCLUDED.full_name
                RETURNING id, full_name, email;
                """,
                ("Alex Morgan", "alex@example.com"),
            )

            patient = cursor.fetchone()

            # Insert a fictional test doctor
            cursor.execute(
                """
                INSERT INTO doctors (full_name, specialty, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (email)
                DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    specialty = EXCLUDED.specialty
                RETURNING id, full_name, specialty;
                """,
                ("Dr Sara Khan", "General Practice",
                 "sara@example.com"),
            )

            doctor = cursor.fetchone()

        connection.commit()

        print("Patient added:", patient)
        print("Doctor added:", doctor)

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    seed_data()
