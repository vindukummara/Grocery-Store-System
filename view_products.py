import streamlit as st
import pandas as pd
import os


def view_products():

    st.title("📋 View Products")

    # Check if products.csv exists
    if not os.path.exists("products.csv"):
        st.warning("No products available.")
        return

    products = pd.read_csv("products.csv")

    if products.empty:
        st.warning("No products found.")
        return

    # Search Product
    search = st.text_input("🔍 Search Product")

    if search:
        products = products[
            products["Product"].str.contains(search, case=False, na=False)
        ]

    st.subheader("📦 Product List")

    st.dataframe(products, use_container_width=True)

    st.write(f"**Total Products:** {len(products)}")

    # Show product image
    st.subheader("🖼️ Product Images")

    for _, row in products.iterrows():

        st.markdown("---")

        col1, col2 = st.columns([1, 3])

        with col1:

            image_path = row["Image"]

            if (
                isinstance(image_path, str)
                and image_path != ""
                and os.path.exists(image_path)
            ):
                st.image(image_path, width=120)
            else:
                st.write("No Image")

        with col2:

            st.write(f"**Product ID:** {row['ProductID']}")
            st.write(f"**Product:** {row['Product']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Price:** ₹{row['Price']}")
            st.write(f"**Stock:** {row['Stock']}")