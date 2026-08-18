import streamlit as st
import pandas as pd
import os

from database import get_connection


def view_products():

    st.header("📋 View Products")

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
        ORDER BY ProductID
    """

    products = pd.read_sql_query(query, conn)

    conn.close()

    if products.empty:

        st.info("📦 No products found.")

        return

    st.success(
        f"✅ {len(products)} product(s) found."
    )

    # -----------------------------
    # Display Products
    # -----------------------------

    for _, product in products.iterrows():

        col1, col2 = st.columns([1, 3])

        with col1:

            image_path = product["Image"]

            if (
                image_path
                and isinstance(image_path, str)
                and os.path.exists(image_path)
            ):

                st.image(
                    image_path,
                    width=120
                )

            else:

                st.write("🖼️ No Image")

        with col2:

            st.subheader(
                f"{product['ProductID']} - {product['Product']}"
            )

            st.write(
                f"**Category:** {product['Category']}"
            )

            st.write(
                f"**Price:** ₹{product['Price']:.2f}"
            )

            st.write(
                f"**Stock:** {product['Stock']}"
            )

        st.markdown("---")

    # -----------------------------
    # Table View
    # -----------------------------

    st.subheader("📊 Product Table")

    st.dataframe(
        products,
        use_container_width=True
    )