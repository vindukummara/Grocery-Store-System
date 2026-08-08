import streamlit as st
import pandas as pd
import os


def dashboard():

    st.title("🏪 Grocery Store Dashboard")

    # Products Count
    if os.path.exists("products.csv"):
        products = pd.read_csv("products.csv")
        total_products = len(products)
        total_stock = products["Stock"].sum()
    else:
        total_products = 0
        total_stock = 0

    # Sales Count
    if os.path.exists("sales.csv"):
        sales = pd.read_csv("sales.csv")
        total_sales = len(sales)
        total_revenue = sales["Total"].sum()
    else:
        total_sales = 0
        total_revenue = 0

    # Customers Count
    if os.path.exists("customers.csv"):
        customers = pd.read_csv("customers.csv")
        total_customers = len(customers)
    else:
        total_customers = 0

    # Suppliers Count
    if os.path.exists("suppliers.csv"):
        suppliers = pd.read_csv("suppliers.csv")
        total_suppliers = len(suppliers)
    else:
        total_suppliers = 0

    # Dashboard Cards
    col1, col2 = st.columns(2)

    with col1:
        st.metric("📦 Total Products", total_products)
        st.metric("🛒 Total Sales", total_sales)
        st.metric("👥 Customers", total_customers)

    with col2:
        st.metric("📦 Stock Available", total_stock)
        st.metric("💰 Total Revenue (₹)", total_revenue)
        st.metric("🚚 Suppliers", total_suppliers)

    st.markdown("---")

    st.subheader("📊 Quick Summary")

    st.write(f"✅ Total Products : **{total_products}**")
    st.write(f"✅ Total Stock : **{total_stock}**")
    st.write(f"✅ Total Sales : **{total_sales}**")
    st.write(f"✅ Total Revenue : **₹{total_revenue:.2f}**")
    st.write(f"✅ Total Customers : **{total_customers}**")
    st.write(f"✅ Total Suppliers : **{total_suppliers}**")

    st.markdown("---")

    st.success("Welcome to the Grocery Store Management System!")