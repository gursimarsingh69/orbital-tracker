
from app.database.session import test_connection

try:
    version = test_connection()

    print("\nORBITWATCH DATABASE CONNECTION")
    print("==============================")
    print("Status: Connected")
    print("Database: orbitwatch")
    print("PostgreSQL version:")
    print(version)

except Exception as error:
    print("Database connection failed!")
    print(error)
