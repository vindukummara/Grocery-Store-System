import streamlit as st
from database import get_connection


def update_product():

    st.header("✏️ Update Product")

    # Get products
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ProductID, Product
        FROM products
        ORDER BY ProductID
    """)

    products = cursor.fetchall()
    conn.close()

    if not products:
        st.warning("No products available.")
        return

    # Product selection
    product_options = {
        f"{product_id} - {product_name}": product_id
        for product_id, product_name in products
    }

    selected_product = st.selectbox(
        "Select Product",
        list(product_options.keys())
    )

    product_id = product_options[selected_product]

    # Get selected product
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Product, Category, Price, Stock
        FROM products
        WHERE ProductID = ?
    """, (product_id,))

    product = cursor.fetchone()
    conn.close()

    if product is None:
        st.error("Product not found.")
        return

    current_name = product[0]
    current_category = product[1]
    current_price = product[2]
    current_stock = product[3]

    # Update fields
    product_name = st.text_input(
        "Product Name",
        value=current_name
    )

    categories = [
        "Food",
        "Bakery",
        "Dairy",
        "Beverages",
        "Fruits",
        "Vegetables",
        "Snacks",
        "Personal Care",
        "Household",
        "Other"
    ]

    category_index = (
        categories.index(current_category)
        if current_category in categories
        else 0
    )

    category = st.selectbox(
        "Category",
        categories,
        index=category_index
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        value=float(current_price),
        step=0.01,
        format="%.2f"
    )

    stock = st.number_input(
        "Stock",
        min_value=0,
        value=int(current_stock),
        step=1
    )

    # Update button
    if st.button("💾 Update Product", type="primary"):

        if not product_name.strip():
            st.warning("Product name cannot be empty.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE products
                SET Product = ?,
                    Category = ?,
                    Price = ?,
                    Stock = ?
                WHERE ProductID = ?
            """, (
                product_name.strip(),
                category,
                price,
                stock,
                product_id
            ))

            conn.commit()

            if cursor.rowcount > 0:
                st.success("✅ Product updated successfully!")
            else:
                st.warning("⚠️ No product was updated.")

            conn.close()

        except Exception as e:
            st.error(f"❌ Update failed: {e}")