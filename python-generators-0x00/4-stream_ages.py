import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator that yields one user age at a time from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor: 
            yield age  

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def compute_average_age():
    """
    Computes average age using the age generator (memory-efficient).
    """
    total = 0
    count = 0
    for age in stream_user_ages():  
        total += age
        count += 1

    return total / count if count else None


if __name__ == "__main__":
    avg = compute_average_age()
    if avg is not None:
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No user data found.")
