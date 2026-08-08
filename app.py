import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Grocery Store Management System",
    page_icon="🛒",
    layout="wide"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =====================================================
# IMPORT MODULES
# =====================================================

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
# LOGIN
# =====================================================

if not st.session_state.logged_in:
    login()
    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🛒 Grocery Store")
st.sidebar.success("Welcome Admin")

menu = st.sidebar.radio(
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
        "👥 Customer Management",
        "🚚 Supplier Management",
        "🚪 Logout"
    ]
)


# =====================================================
# MAIN TITLE
# =====================================================

st.title("🛒 Grocery Store Management System")
st.markdown("---")


# =====================================================
# MODULE NAVIGATION
# =====================================================

if menu == "🏠 Dashboard":

    dashboard()


elif menu == "➕ Add Product":

    add_product()


elif menu == "📋 View Products":

    view_products()


elif menu == "✏️ Update Product":

    update_product()


elif menu == "🗑️ Delete Product":

    delete_product()


elif menu == "🔍 Search Product":

    search_product()


elif menu == "🛒 Billing":

    billing()


elif menu == "📉 Low Stock":

    low_stock()


elif menu == "📊 Sales Report":

    sales_report()


elif menu == "👥 Customer Management":

    customer()


elif menu == "🚚 Supplier Management":

    supplier()


elif menu == "🚪 Logout":

    logout()