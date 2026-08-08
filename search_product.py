import streamlit as st
import pandas as pd
import os


def search_product():

    st.title("🔍 Search Product")

    # Check if products.csv exists
    if not os.path.exists("products.csv"):
        st.warning("products.csv not found.")
        return

    products = pd.read_csv("products.csv")

    if products.empty:
        st.warning("No products available.")
        return

    # Search box
    search = st.text_input("Enter Product Name")

    if st.button("Search"):

        if search.strip() == "":
            st.warning("Please enter a product name.")
            return

        result = products[
            products["Product"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        if result.empty:
            st.error("❌ Product not found.")

        else:

            st.success(f"✅ {len(result)} Product(s) Found")

            for _, row in result.iterrows():

                st.markdown("---")

                col1, col2 = st.columns([1, 3])

                with col1:

                    image_path = row["Image"]

                    if (
                        isinstance(image_path, str)
                        and image_path != ""
                        and os.path.exists(image_path)
                    ):
                        st.image(image_path, width=150)
                    else:
                        st.write("No Image")

                with col2:

                    st.write(f"**Product ID:** {row['ProductID']}")
                    st.write(f"**Product:** {row['Product']}")
                    st.write(f"**Category:** {row['Category']}")
                    st.write(f"**Price:** ₹{row['Price']}")
                    st.write(f"**Stock:** {row['Stock']}")