import streamlit as st

from database import create_tables
from login import login
from logout import logout
from dashboard import dashboard
from add_product import add_product
from view_products import view_products
from update_product import update_product
from delete_product import delete_product
from search_product import search_product
from billing import billing
from low_stock import low_stock
from sales_report import sales_report
from customer import customer
from supplier import supplier


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Grocery Store Management System",
    page_icon="🛒",
    layout="wide"
)


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

create_tables()


# =====================================================
# INITIALIZE SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    login()

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🛒 Grocery Store")

st.sidebar.success(
    f"Welcome, {st.session_state.username}"
)


# =====================================================
# MENU
# =====================================================

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",
        "➕ Add Product",
        "📋 View Products",
        "✏️ Update Product",
        "🗑️ Delete Product",
        "🔍 Search Product",
        "🛒 Billing",
        "📉 Low Stock",
        "📊 Sales Report",
        "👥 Customers",
        "🚚 Suppliers",
        "🚪 Logout"
    ]
)


# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    dashboard()


# =====================================================
# ADD PRODUCT
# =====================================================

elif menu == "➕ Add Product":

    add_product()


# =====================================================
# VIEW PRODUCTS
# =====================================================

elif menu == "📋 View Products":

    view_products()


# =====================================================
# UPDATE PRODUCT
# =====================================================

elif menu == "✏️ Update Product":

    update_product()


# =====================================================
# DELETE PRODUCT
# =====================================================

elif menu == "🗑️ Delete Product":

    delete_product()


# =====================================================
# SEARCH PRODUCT
# =====================================================

elif menu == "🔍 Search Product":

    search_product()


# =====================================================
# BILLING
# =====================================================

elif menu == "🛒 Billing":

    billing()


# =====================================================
# LOW STOCK
# =====================================================

elif menu == "📉 Low Stock":

    low_stock()


# =====================================================
# SALES REPORT
# =====================================================

elif menu == "📊 Sales Report":

    sales_report()


# =====================================================
# CUSTOMER MANAGEMENT
# =====================================================

elif menu == "👥 Customers":

    customer()


# =====================================================
# SUPPLIER MANAGEMENT
# =====================================================

elif menu == "🚚 Suppliers":

    supplier()


# =====================================================
# LOGOUT
# =====================================================

elif menu == "🚪 Logout":

    logout()