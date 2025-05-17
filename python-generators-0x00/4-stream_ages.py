import mysql.connector
from mysql.connector import Error

def stream_ages():
    """
    Generator that yields one 'age' value at a time from the user_data table.
    This avoids loading the full dataset into memory.
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
        print(f"Error streaming ages: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def average_age():
    """
    Computes the average age using a generator for memory-efficient processing.
    """
    total = 0
    count = 0

    for age in stream_ages(): 
        total += age
        count += 1

    return total / count if count else None
