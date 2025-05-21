import sqlite3

class DatabaseConnection:
    def __init__(self, users):
        self.db_name = users
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
        self.conn.commit()
        self.conn.close()

# Example usage
with DatabaseConnection("users.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
