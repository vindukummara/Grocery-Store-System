import streamlit as st
import pandas as pd
import os


def add_product():

    st.title("➕ Add Product")

    # Create products.csv if it doesn't exist
    if not os.path.exists("products.csv"):
        df = pd.DataFrame(columns=[
            "ProductID",
            "Product",
            "Category",
            "Price",
            "Stock",
            "Image"
        ])
        df.to_csv("products.csv", index=False)

    products = pd.read_csv("products.csv")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1
    )

    product_name = st.text_input("Product Name")

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

    price = st.number_input(
        "Price (₹)",
        min_value=0.0,
        format="%.2f"
    )

    stock = st.number_input(
        "Stock Quantity",
        min_value=0,
        step=1
    )

    image = st.file_uploader(
        "Upload Product Image",
        type=["jpg", "jpeg", "png"]
    )

    image_path = ""

    if image is not None:

        # Create images folder
        if not os.path.exists("images"):
            os.makedirs("images")

        image_path = os.path.join("images", image.name)

        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

        st.image(image, width=200)

    if st.button("Add Product"):

        # Check duplicate Product ID
        if product_id in products["ProductID"].values:
            st.error("❌ Product ID already exists.")

        elif product_name.strip() == "":
            st.warning("Please enter a product name.")

        else:

            new_product = pd.DataFrame({

                "ProductID": [product_id],
                "Product": [product_name],
                "Category": [category],
                "Price": [price],
                "Stock": [stock],
                "Image": [image_path]

            })

            products = pd.concat(
                [products, new_product],
                ignore_index=True
            )

            products.to_csv(
                "products.csv",
                index=False
            )

            st.success("✅ Product Added Successfully!")

            st.subheader("Current Products")

            st.dataframe(
                products,
                use_container_width=True
            )