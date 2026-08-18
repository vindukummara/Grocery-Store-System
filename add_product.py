import streamlit as st
import os

from database import get_connection


def add_product():

    st.header("➕ Add Product")

    # -----------------------------
    # Product ID
    # -----------------------------
    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1
    )

    # -----------------------------
    # Product Name
    # -----------------------------
    product_name = st.text_input("Product Name")

    # -----------------------------
    # Category
    # -----------------------------
    category = st.selectbox(
        "Category",
        [
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
    )

    # -----------------------------
    # Price
    # -----------------------------
    price = st.number_input(
        "Price",
        min_value=0.0,
        format="%.2f"
    )

    # -----------------------------
    # Stock
    # -----------------------------
    stock = st.number_input(
        "Stock",
        min_value=0,
        step=1
    )

    # -----------------------------
    # Product Image
    # -----------------------------
    image = st.file_uploader(
        "Upload Product Image",
        type=["png", "jpg", "jpeg"]
    )

    image_path = ""

    if image is not None:

        if not os.path.exists("images"):
            os.makedirs("images")

        image_path = os.path.join(
            "images",
            image.name
        )

        with open(image_path, "wb") as file:
            file.write(image.getbuffer())

        st.image(
            image,
            width=150
        )

    # -----------------------------
    # Add Product
    # -----------------------------
    if st.button("Add Product"):

        if product_name.strip() == "":
            st.warning(
                "⚠️ Please enter a product name."
            )

        else:

            conn = get_connection()
            cursor = conn.cursor()

            # Check Product ID
            cursor.execute(
                """
                SELECT ProductID
                FROM products
                WHERE ProductID = ?
                """,
                (product_id,)
            )

            existing_product = cursor.fetchone()

            if existing_product:

                st.error(
                    "❌ Product ID already exists."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO products
                    (
                        ProductID,
                        Product,
                        Category,
                        Price,
                        Stock,
                        Image
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        product_id,
                        product_name,
                        category,
                        price,
                        stock,
                        image_path
                    )
                )

                conn.commit()

                st.success(
                    "✅ Product Added Successfully!"
                )

            conn.close()