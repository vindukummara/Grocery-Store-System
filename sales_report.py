import streamlit as st
import pandas as pd
import os


def sales_report():

    st.title("📊 Sales Report")

    # Check if sales.csv exists
    if not os.path.exists("sales.csv"):
        st.warning("sales.csv not found.")
        return

    sales = pd.read_csv("sales.csv")

    if sales.empty:
        st.warning("No sales available.")
        return

    # --------------------------
    # Summary
    # --------------------------

    total_orders = len(sales)
    total_quantity = sales["Quantity"].sum()
    total_revenue = sales["Total"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🛒 Total Orders", total_orders)

    with col2:
        st.metric("📦 Products Sold", total_quantity)

    with col3:
        st.metric("💰 Total Revenue", f"₹{total_revenue:.2f}")

    st.markdown("---")

    # --------------------------
    # Sales Chart
    # --------------------------

    st.subheader("📈 Sales Revenue Chart")

    st.bar_chart(sales["Total"])

    st.markdown("---")

    # --------------------------
    # Products Sold Chart
    # --------------------------

    st.subheader("📦 Products Sold")

    product_chart = sales.groupby("Product")["Quantity"].sum()

    st.bar_chart(product_chart)

    st.markdown("---")

    # --------------------------
    # Sales Data
    # --------------------------

    st.subheader("📋 Sales Records")

    st.dataframe(
        sales,
        use_container_width=True
    )

    # --------------------------
    # Download CSV
    # --------------------------

    csv = sales.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Sales Report",
        data=csv,
        file_name="sales_report.csv",
        mime="text/csv"
    )