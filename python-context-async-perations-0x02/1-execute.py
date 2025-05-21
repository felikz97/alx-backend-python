import sqlite3

class ExecuteQuery:
    def __init__(self, users, query, params=None):
        self.db_name = users
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # this goes into the variable after 'as' in 'with' statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        self.conn.commit()
        self.conn.close()


# Setup: create a users table with age column (if not already created)
with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [("Felikz", 26), ("Dabitha", 21), ("Jamin", 31), ("David", 22)]
    )
    conn.commit()


# 🧪 Usage of context manager with "with" statement
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users", query, params) as result:
    print("Query Result:")
    for row in result:
        print(row)
