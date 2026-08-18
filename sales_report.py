import streamlit as st
import pandas as pd

from database import get_connection


def sales_report():

    st.header("📊 Sales Report")

    # =====================================================
    # GET SALES FROM SQLITE
    # =====================================================

    conn = get_connection()

    query = """
        SELECT
            s.SaleID,
            s.Date,
            s.Time,
            s.ProductID,
            p.Product,
            s.Quantity,
            s.Price,
            s.Total
        FROM sales s
        LEFT JOIN products p
            ON s.ProductID = p.ProductID
        ORDER BY s.SaleID DESC
    """

    sales = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    # =====================================================
    # CHECK SALES
    # =====================================================

    if sales.empty:

        st.info("📦 No sales records found.")

        return

    # =====================================================
    # SUMMARY
    # =====================================================

    total_sales = sales["Total"].sum()
    total_items = sales["Quantity"].sum()
    total_transactions = sales["SaleID"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Sales",
            f"₹{total_sales:.2f}"
        )

    with col2:
        st.metric(
            "📦 Items Sold",
            int(total_items)
        )

    with col3:
        st.metric(
            "🧾 Transactions",
            total_transactions
        )

    st.markdown("---")

    # =====================================================
    # SALES TABLE
    # =====================================================

    st.subheader("📋 Sales History")

    st.dataframe(
        sales,
        use_container_width=True
    )

    # =====================================================
    # DAILY SALES
    # =====================================================

    st.subheader("📅 Daily Sales")

    daily_sales = (
        sales.groupby("Date")["Total"]
        .sum()
        .reset_index()
    )

    daily_sales.columns = [
        "Date",
        "Total Sales"
    ]

    st.dataframe(
        daily_sales,
        use_container_width=True
    )

    # =====================================================
    # PRODUCT SALES
    # =====================================================

    st.subheader("📦 Product-wise Sales")

    product_sales = (
        sales.groupby("Product")
        .agg(
            Quantity_Sold=("Quantity", "sum"),
            Total_Sales=("Total", "sum")
        )
        .reset_index()
    )

    product_sales = product_sales.sort_values(
        by="Total_Sales",
        ascending=False
    )

    st.dataframe(
        product_sales,
        use_container_width=True
    )

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    csv_data = sales.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Sales Report",
        data=csv_data,
        file_name="sales_report.csv",
        mime="text/csv"
    )