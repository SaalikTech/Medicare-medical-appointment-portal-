
from getpass import getpass


from database import create_user


def main():
    email = input("Email address: ").strip()

    role = input(
        "Account role (patient/admin): "
    ).strip().lower()

    if role not in ("patient", "admin"):
        print("Invalid role.")
        return

    if role == "admin":
        print(
            "Only run this script as an authorised administrator."
        )

    password = getpass("Password (minimum 12 characters): ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        user_id = create_user(email, password, role)
        print(f"Account created successfully. User ID: {user_id}")

    except ValueError as error:
        print(f"Could not create account: {error}")

    except Exception:
        print(
            "Account creation failed. "
            "Check the email, database connection and server logs."
        )


if __name__ == "__main__":
    main()

#admin@test.com coolicecream 
#patient thewateriscold