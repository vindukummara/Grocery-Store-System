import streamlit as st
import pandas as pd

from database import get_connection


def low_stock():

    st.header("📉 Low Stock Alert")

    # -----------------------------
    # Low Stock Limit
    # -----------------------------
    stock_limit = st.number_input(
        "Show products with stock less than or equal to:",
        min_value=0,
        value=10,
        step=1
    )

    # -----------------------------
    # Get Products from SQLite
    # -----------------------------
    conn = get_connection()

    query = """
        SELECT
            ProductID,
            Product,
            Category,
            Price,
            Stock,
            Image
        FROM products
        WHERE Stock <= ?
        ORDER BY Stock ASC
    """

    products = pd.read_sql_query(
        query,
        conn,
        params=(stock_limit,)
    )

    conn.close()

    # -----------------------------
    # Display Results
    # -----------------------------
    if products.empty:

        st.success(
            "✅ No products have low stock."
        )

        return

    st.warning(
        f"⚠️ {len(products)} product(s) have low stock."
    )

    # -----------------------------
    # Low Stock Table
    # -----------------------------
    st.dataframe(
        products,
        use_container_width=True
    )

    # -----------------------------
    # Product Details
    # -----------------------------
    st.subheader("📦 Low Stock Products")

    for _, product in products.iterrows():

        col1, col2 = st.columns([1, 4])

        with col1:

            image_path = product["Image"]

            if (
                image_path
                and isinstance(image_path, str)
            ):

                try:
                    st.image(
                        image_path,
                        width=100
                    )
                except Exception:
                    st.write("🖼️ No Image")

            else:
                st.write("🖼️ No Image")

        with col2:

            st.write(
                f"**Product:** {product['Product']}"
            )

            st.write(
                f"**Category:** {product['Category']}"
            )

            st.write(
                f"**Price:** ₹{product['Price']:.2f}"
            )

            st.error(
                f"⚠️ Stock: {product['Stock']}"
            )

        st.markdown("---")