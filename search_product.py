import streamlit as st
import pandas as pd
import os

from database import get_connection


def search_product():

    st.header("🔍 Search Product")

    # -----------------------------
    # Search Input
    # -----------------------------
    search_text = st.text_input(
        "Enter product name or category"
    )

    if st.button("🔍 Search"):

        if search_text.strip() == "":
            st.warning("⚠️ Please enter a product name or category.")
            return

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
            WHERE Product LIKE ?
               OR Category LIKE ?
            ORDER BY ProductID
        """

        search_value = f"%{search_text}%"

        products = pd.read_sql_query(
            query,
            conn,
            params=(search_value, search_value)
        )

        conn.close()

        # -----------------------------
        # Search Results
        # -----------------------------
        if products.empty:

            st.warning(
                f"❌ No products found for '{search_text}'."
            )

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
        # Results Table
        # -----------------------------
        st.subheader("📊 Search Results")

        st.dataframe(
            products,
            use_container_width=True
        )