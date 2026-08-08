import streamlit as st
import pandas as pd
import os


def low_stock():

    st.title("📉 Low Stock Alert")

    # Check if products.csv exists
    if not os.path.exists("products.csv"):
        st.error("❌ products.csv not found.")
        return

    products = pd.read_csv("products.csv")

    if products.empty:
        st.warning("No products available.")
        return

    # User selects the low stock limit
    threshold = st.slider(
        "Select Low Stock Limit",
        min_value=1,
        max_value=50,
        value=10
    )

    # Find low stock products
    low_stock_products = products[
        products["Stock"] <= threshold
    ]

    if low_stock_products.empty:
        st.success("✅ No Low Stock Products.")
    else:
        st.warning(f"⚠️ {len(low_stock_products)} product(s) have low stock.")

        st.dataframe(
            low_stock_products,
            use_container_width=True
        )

        st.subheader("📦 Low Stock Products")

        for _, row in low_stock_products.iterrows():

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
                st.write(f"**Stock Remaining:** {row['Stock']}")

                if row["Stock"] == 0:
                    st.error("❌ Out of Stock")
                elif row["Stock"] <= 5:
                    st.error("🔴 Critical Stock")
                else:
                    st.warning("🟡 Low Stock")