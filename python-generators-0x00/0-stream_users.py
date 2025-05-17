import mysql.connector
from mysql.connector import Error

def stream_users():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254',
            database='ALX_prodev'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data;")

            for row in cursor:  # Only 1 loop here
                yield row

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Database error: {e}")
        return