import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """Fetches a single page of users from DB at a given offset."""
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
        rows = cursor.fetchall()
        return rows

    except Error as e:
        print(f"Error fetching users: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lazy_paginate(page_size):
    """Yields pages of users one at a time using offset-based pagination."""
    offset = 0
    while True: 
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  
        offset += page_size
