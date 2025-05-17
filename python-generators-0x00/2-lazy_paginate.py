import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254', 
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"  
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

    except Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily yields pages of users from the user_data table.
    Uses only one loop.
    """
    offset = 0
    while True: 
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page 
        offset += page_size
