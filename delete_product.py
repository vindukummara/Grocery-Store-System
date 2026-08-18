import streamlit as st
from database import get_connection


def delete_product():

    st.header("🗑️ Delete Product")

    # Get products
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ProductID, Product, Category, Price, Stock
        FROM products
        ORDER BY ProductID
    """)

    products = cursor.fetchall()
    conn.close()

    if not products:
        st.info("📦 No products available.")
        return

    # Product selection
    product_options = {
        f"{product_id} - {product_name}": product_id
        for product_id, product_name, category, price, stock in products
    }

    selected_product = st.selectbox(
        "Select Product to Delete",
        list(product_options.keys())
    )

    product_id = product_options[selected_product]

    # Show selected product
    selected_data = next(
        product for product in products
        if product[0] == product_id
    )

    st.write("### Product Details")
    st.write(f"**Product:** {selected_data[1]}")
    st.write(f"**Category:** {selected_data[2]}")
    st.write(f"**Price:** ₹{selected_data[3]}")
    st.write(f"**Stock:** {selected_data[4]}")

    st.warning(
        "⚠️ Deleting this product cannot be undone."
    )

    # Confirmation
    confirm = st.checkbox(
        "I confirm that I want to delete this product."
    )

    if st.button("🗑️ Delete Product", type="primary"):

        if not confirm:
            st.warning(
                "Please confirm the deletion first."
            )
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM products
                WHERE ProductID = ?
            """, (product_id,))

            conn.commit()

            if cursor.rowcount > 0:
                st.success(
                    "✅ Product deleted successfully!"
                )
            else:
                st.error(
                    "❌ Product could not be deleted."
                )

            conn.close()

            st.rerun()

        except Exception as e:
            st.error(f"❌ Delete failed: {e}")