import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetches one page of user records using LIMIT and OFFSET.
    Returns a list of rows.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254', 
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT user_id, name, email, age
            FROM user_data
            ORDER BY user_id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

    except Error as e:
        print(f"Error during pagination: {e}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    offset = 0
    while True: 
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  
        offset += page_size
