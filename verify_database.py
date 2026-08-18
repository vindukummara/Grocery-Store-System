import sqlite3

conn = sqlite3.connect("grocery_store.db")
cursor = conn.cursor()

print("===== DATABASE VERIFICATION =====")

cursor.execute("SELECT COUNT(*) FROM products")
print("Products:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM customers")
print("Customers:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM suppliers")
print("Suppliers:", cursor.fetchone()[0])

print("=================================")

conn.close()