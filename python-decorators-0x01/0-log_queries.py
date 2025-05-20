import sqlite3
import functools
from datetime import datetime

# ---- Decorator to log SQL queries with timestamp ----
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else "<no query>"
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        print(f"[{timestamp}] [SQL LOG] Executing: {query}")
        return func(*args, **kwargs)
    return wrapper

# ---- Create and populate users table if not exists ----
def setup_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    now = datetime.now().isoformat()
    cursor.executemany("""
        INSERT OR IGNORE INTO users (username, email, created_at)
        VALUES (?, ?, ?)
    """, [
        ('felikz', 'felikz@gmail.com', now),
        ('dabitha', 'dabitha@gmail.com', now),
        ('Daizy', 'daizy@gmail.com', now),
    ])
    conn.commit()
    conn.close()

# ---- Function to fetch all users with logging ----
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ---- Run ----
if __name__ == "__main__":
    setup_users_table()
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
