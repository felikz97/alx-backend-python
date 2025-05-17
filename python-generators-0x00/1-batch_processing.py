import mysql.connector
from mysql.connector import Error
import sys
processing = __import__('1-batch_processing')
def stream_users_in_batches(batch_size):
    """Yields batches of users from the DB using one loop."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  #  Yield each batch (1 loop here)

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """Filters and processes users over age 25 using 1 additional loop."""
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        filtered = (user for user in batch if user['age'] > 25)  # generator expression, not a loop
        for user in filtered:  # 3rd loop (total loop count: 3)
            print(user)
