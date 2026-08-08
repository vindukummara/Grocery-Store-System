import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("grocery.db")

cursor = conn.cursor()

# Create Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    product TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
""")

conn.commit()
conn.close()