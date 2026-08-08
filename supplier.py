import streamlit as st
import pandas as pd
import os


def supplier():

    st.title("🚚 Supplier Management")

    # Create suppliers.csv if it doesn't exist
    if not os.path.exists("suppliers.csv"):
        df = pd.DataFrame(columns=[
            "SupplierID",
            "SupplierName",
            "Phone",
            "Address",
            "Products"
        ])
        df.to_csv("suppliers.csv", index=False)

    suppliers = pd.read_csv("suppliers.csv")

    # -----------------------------
    # Add Supplier
    # -----------------------------
    st.subheader("➕ Add Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1
    )

    supplier_name = st.text_input("Supplier Name")

    phone = st.text_input("Phone Number")

    address = st.text_area("Address")

    products = st.text_input(
        "Products Supplied"
    )

    if st.button("Add Supplier"):

        if supplier_id in suppliers["SupplierID"].values:
            st.error("❌ Supplier ID already exists.")

        elif supplier_name.strip() == "":
            st.warning("Please enter the supplier name.")

        else:

            new_supplier = pd.DataFrame({

                "SupplierID": [supplier_id],
                "SupplierName": [supplier_name],
                "Phone": [phone],
                "Address": [address],
                "Products": [products]

            })

            suppliers = pd.concat(
                [suppliers, new_supplier],
                ignore_index=True
            )

            suppliers.to_csv(
                "suppliers.csv",
                index=False
            )

            st.success("✅ Supplier Added Successfully!")

    st.markdown("---")

    # -----------------------------
    # Search Supplier
    # -----------------------------
    st.subheader("🔍 Search Supplier")

    search = st.text_input("Enter Supplier Name")

    if search:

        result = suppliers[
            suppliers["SupplierName"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            result,
            use_container_width=True
        )

    st.markdown("---")

    # -----------------------------
    # Supplier List
    # -----------------------------
    st.subheader("📋 Supplier List")

    st.dataframe(
        suppliers,
        use_container_width=True
    )