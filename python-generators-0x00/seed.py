import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Felikz@254',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to database")
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def list_tables_and_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found.")
            return

        for (table_name,) in tables:
            print(f"\nTable: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print(" (no data)")

        cursor.close()

    except Error as e:
        print(f"Error reading tables: {e}")

def main():
    connection = connect_to_db()
    if connection:
        list_tables_and_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
