from database import get_connection

try:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            print("Connected to:", cursor.fetchone()[0])

except Exception as error:
    print("Connection failed:", error)