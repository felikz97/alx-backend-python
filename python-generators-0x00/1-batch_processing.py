import mysql.connector
from mysql.connector import Error

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

        while True:  # ✅ loop 1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """Filters users over age 25 and returns them."""
    results = []

    for batch in stream_users_in_batches(batch_size):  # ✅ loop 2
        filtered = (user for user in batch if user['age'] > 25)
        for user in filtered:  # ✅ loop 3
            print(user)         # optional: log or process
            results.append(user)

    return results  # ✅ REQUIRED: return filtered results
