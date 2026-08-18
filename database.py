import sqlite3

DATABASE = "grocery_store.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # =================================================
    # PRODUCTS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            ProductID INTEGER PRIMARY KEY,
            Product TEXT NOT NULL,
            Category TEXT NOT NULL,
            Price REAL NOT NULL,
            Stock INTEGER NOT NULL,
            Image TEXT
        )
    """)

    # =================================================
    # SALES TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            Time TEXT NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            Price REAL NOT NULL,
            Total REAL NOT NULL,

            FOREIGN KEY (ProductID)
            REFERENCES products(ProductID)
        )
    """)

    # =================================================
    # CUSTOMERS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            CustomerID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Phone TEXT,
            Address TEXT
        )
    """)

    # =================================================
    # SUPPLIERS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            SupplierID INTEGER PRIMARY KEY,
            SupplierName TEXT NOT NULL,
            Phone TEXT,
            Address TEXT
        )
    """)

    # =================================================
    # USERS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            SecurityQuestion TEXT NOT NULL,
            SecurityAnswer TEXT NOT NULL
        )
    """)

    # =================================================
    # SAVE CHANGES
    # =================================================

    conn.commit()
    conn.close()