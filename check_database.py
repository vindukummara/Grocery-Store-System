from database import get_connection, create_tables


create_tables()

conn = get_connection()
cursor = conn.cursor()


print("\n===================================")
print("      SQLITE DATABASE CHECK")
print("===================================\n")


# Products
cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]

print(f"📦 Products    : {product_count}")


# Sales
cursor.execute("SELECT COUNT(*) FROM sales")
sales_count = cursor.fetchone()[0]

print(f"🧾 Sales       : {sales_count}")


# Customers
cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]

print(f"👥 Customers   : {customer_count}")


# Suppliers
cursor.execute("SELECT COUNT(*) FROM suppliers")
supplier_count = cursor.fetchone()[0]

print(f"🚚 Suppliers   : {supplier_count}")


print("\n===================================")
print("      PRODUCT DATA")
print("===================================\n")

cursor.execute("""
    SELECT
        ProductID,
        Product,
        Category,
        Price,
        Stock
    FROM products
    ORDER BY ProductID
""")

products = cursor.fetchall()

for product in products:
    print(product)


print("\n===================================")
print("      SALES DATA")
print("===================================\n")

cursor.execute("""
    SELECT
        SaleID,
        Date,
        ProductID,
        Quantity,
        Price,
        Total
    FROM sales
    ORDER BY SaleID
""")

sales = cursor.fetchall()

for sale in sales:
    print(sale)


conn.close()

print("\n===================================")
print("✅ Database verification completed")
print("===================================")