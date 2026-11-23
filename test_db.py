from database import get_connection

try:
    connection = get_connection()

    print("MySQL Database Connected Successfully!")

    connection.close()

except Exception as e:
    print("Database Connection Failed!")
    print(e)