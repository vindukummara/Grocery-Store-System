import streamlit as st
import pandas as pd
import os


def customer():

    st.title("👥 Customer Management")

    # Create customers.csv if it doesn't exist
    if not os.path.exists("customers.csv"):
        df = pd.DataFrame(columns=[
            "CustomerID",
            "Name",
            "Phone",
            "Address"
        ])
        df.to_csv("customers.csv", index=False)

    customers = pd.read_csv("customers.csv")

    # -----------------------------
    # Add Customer
    # -----------------------------

    st.subheader("➕ Add Customer")

    customer_id = st.number_input(
        "Customer ID",
        min_value=1,
        step=1
    )

    name = st.text_input("Customer Name")

    phone = st.text_input("Phone Number")

    address = st.text_area("Address")

    if st.button("Add Customer"):

        if customer_id in customers["CustomerID"].values:
            st.error("❌ Customer ID already exists.")

        elif name.strip() == "":
            st.warning("Please enter the customer name.")

        else:

            new_customer = pd.DataFrame({

                "CustomerID": [customer_id],
                "Name": [name],
                "Phone": [phone],
                "Address": [address]

            })

            customers = pd.concat(
                [customers, new_customer],
                ignore_index=True
            )

            customers.to_csv(
                "customers.csv",
                index=False
            )

            st.success("✅ Customer Added Successfully!")

    st.markdown("---")

    # -----------------------------
    # Search Customer
    # -----------------------------

    st.subheader("🔍 Search Customer")

    search = st.text_input("Enter Customer Name")

    if search:

        result = customers[
            customers["Name"].str.contains(
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
    # Customer List
    # -----------------------------

    st.subheader("📋 Customer List")

    st.dataframe(
        customers,
        use_container_width=True
    )