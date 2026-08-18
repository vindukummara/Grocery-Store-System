import streamlit as st

from database import get_connection


def dashboard():

    st.header("🏠 Dashboard")

    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # PRODUCT COUNT
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    total_products = cursor.fetchone()[0]

    # =====================================================
    # TOTAL STOCK
    # =====================================================

    cursor.execute("""
        SELECT COALESCE(SUM(Stock), 0)
        FROM products
    """)

    total_stock = cursor.fetchone()[0]

    # =====================================================
    # LOW STOCK COUNT
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE Stock <= 10
    """)

    low_stock_count = cursor.fetchone()[0]

    # =====================================================
    # TOTAL SALES
    # =====================================================

    cursor.execute("""
        SELECT COALESCE(SUM(Total), 0)
        FROM sales
    """)

    total_sales = cursor.fetchone()[0]

    # =====================================================
    # TOTAL TRANSACTIONS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
    """)

    total_transactions = cursor.fetchone()[0]

    # =====================================================
    # TOTAL CUSTOMERS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    total_customers = cursor.fetchone()[0]

    # =====================================================
    # TOTAL SUPPLIERS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM suppliers
    """)

    total_suppliers = cursor.fetchone()[0]

    conn.close()

    # =====================================================
    # DASHBOARD CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Total Products",
            total_products
        )

    with col2:

        st.metric(
            "📊 Total Stock",
            total_stock
        )

    with col3:

        st.metric(
            "💰 Total Sales",
            f"₹{total_sales:.2f}"
        )

    with col4:

        st.metric(
            "🧾 Transactions",
            total_transactions
        )

    st.markdown("---")

    col5, col6, col7 = st.columns(3)

    with col5:

        st.metric(
            "👥 Customers",
            total_customers
        )

    with col6:

        st.metric(
            "🚚 Suppliers",
            total_suppliers
        )

    with col7:

        st.metric(
            "⚠️ Low Stock",
            low_stock_count
        )

    st.markdown("---")

    # =====================================================
    # LOW STOCK ALERT
    # =====================================================

    if low_stock_count > 0:

        st.warning(
            f"⚠️ {low_stock_count} product(s) have low stock."
        )

    else:

        st.success(
            "✅ All products have sufficient stock."
        )

    # =====================================================
    # RECENT SALES
    # =====================================================

    st.subheader("🧾 Recent Sales")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.SaleID,
            s.Date,
            s.Time,
            p.Product,
            s.Quantity,
            s.Price,
            s.Total
        FROM sales s
        LEFT JOIN products p
            ON s.ProductID = p.ProductID
        ORDER BY s.SaleID DESC
        LIMIT 5
    """)

    recent_sales = cursor.fetchall()

    conn.close()

    if recent_sales:

        st.dataframe(
            recent_sales,
            column_config={
                "SaleID": "Sale ID",
                "Date": "Date",
                "Time": "Time",
                "Product": "Product",
                "Quantity": "Quantity",
                "Price": "Price",
                "Total": "Total"
            },
            use_container_width=True
        )

    else:

        st.info(
            "📦 No sales recorded yet."
        )