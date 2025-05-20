import sqlite3
import functools

# ---- Decorator to log SQL queries ----
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else "<no query>"
        print(f"[SQL LOG] About to execute: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def setup_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL
        )
    """)
    cursor.executemany("""
        INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)
    """, [
        ("Felikz", "felikz@gmail.com"),
        ("Dabitha", "dabitha@gmail.com.com"),
        ("Daizy", "daizy@gmail.com"),
    ])
    conn.commit()
    conn.close()

# ---- Main flow ----
if __name__ == "__main__":
    setup_db()  # Run only once to create and populate the table
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
