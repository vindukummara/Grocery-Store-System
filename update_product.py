import streamlit as st
import pandas as pd
import os


def update_product():

    st.title("✏️ Update Product")

    # Check if products.csv exists
    if not os.path.exists("products.csv"):
        st.warning("products.csv not found.")
        return

    products = pd.read_csv("products.csv")

    if products.empty:
        st.warning("No products available.")
        return

    # Select Product
    product_id = st.selectbox(
        "Select Product ID",
        products["ProductID"]
    )

    product = products[products["ProductID"] == product_id].iloc[0]

    # Existing values
    product_name = st.text_input(
        "Product Name",
        value=product["Product"]
    )

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
        ],
        index=[
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
        ].index(product["Category"])
        if product["Category"] in [
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
        else 0
    )

    price = st.number_input(
        "Price (₹)",
        min_value=0.0,
        value=float(product["Price"]),
        format="%.2f"
    )

    stock = st.number_input(
        "Stock",
        min_value=0,
        value=int(product["Stock"])
    )

    image = st.file_uploader(
        "Upload New Image (Optional)",
        type=["jpg", "jpeg", "png"]
    )

    image_path = product["Image"]

    if image is not None:

        if not os.path.exists("images"):
            os.makedirs("images")

        image_path = os.path.join("images", image.name)

        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

        st.image(image, width=150)

    # Update Button
    if st.button("Update Product"):

        products.loc[
            products["ProductID"] == product_id,
            ["Product", "Category", "Price", "Stock", "Image"]
        ] = [
            product_name,
            category,
            price,
            stock,
            image_path
        ]

        products.to_csv(
            "products.csv",
            index=False
        )

        st.success("✅ Product Updated Successfully!")

        st.dataframe(
            products,
            use_container_width=True
        )