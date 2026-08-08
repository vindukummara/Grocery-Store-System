import streamlit as st
import pandas as pd
import os


def delete_product():

    st.title("🗑️ Delete Product")

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

    product = products[
        products["ProductID"] == product_id
    ].iloc[0]

    st.subheader("Product Details")

    st.write(f"**Product ID:** {product['ProductID']}")
    st.write(f"**Product Name:** {product['Product']}")
    st.write(f"**Category:** {product['Category']}")
    st.write(f"**Price:** ₹{product['Price']}")
    st.write(f"**Stock:** {product['Stock']}")

    # Display Product Image
    image_path = product["Image"]

    if (
        isinstance(image_path, str)
        and image_path != ""
        and os.path.exists(image_path)
    ):
        st.image(image_path, width=180)

    st.warning("⚠️ This action cannot be undone.")

    if st.button("Delete Product"):

        products = products[
            products["ProductID"] != product_id
        ]

        products.to_csv(
            "products.csv",
            index=False
        )

        st.success("✅ Product Deleted Successfully!")

        st.dataframe(
            products,
            use_container_width=True
        )