import streamlit as st
import pandas as pd

from database import get_connection


def customer():

    st.header("👥 Customer Management")

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Customer",
            "📋 View Customers",
            "🗑️ Delete Customer"
        ]
    )

    # =====================================================
    # ADD CUSTOMER
    # =====================================================

    with tab1:

        st.subheader("➕ Add Customer")

        customer_id = st.number_input(
            "Customer ID",
            min_value=1,
            step=1
        )

        name = st.text_input(
            "Customer Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        address = st.text_area(
            "Address"
        )

        if st.button(
            "➕ Add Customer",
            key="add_customer"
        ):

            if name.strip() == "":
                st.warning(
                    "⚠️ Please enter customer name."
                )

                return

            conn = get_connection()
            cursor = conn.cursor()

            # Check Customer ID
            cursor.execute(
                """
                SELECT CustomerID
                FROM customers
                WHERE CustomerID = ?
                """,
                (customer_id,)
            )

            existing_customer = cursor.fetchone()

            if existing_customer:

                st.error(
                    "❌ Customer ID already exists."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO customers
                    (
                        CustomerID,
                        Name,
                        Phone,
                        Address
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        customer_id,
                        name,
                        phone,
                        address
                    )
                )

                conn.commit()

                st.success(
                    "✅ Customer added successfully!"
                )

            conn.close()

    # =====================================================
    # VIEW CUSTOMERS
    # =====================================================

    with tab2:

        st.subheader("📋 Customer List")

        conn = get_connection()

        customers = pd.read_sql_query(
            """
            SELECT
                CustomerID,
                Name,
                Phone,
                Address
            FROM customers
            ORDER BY CustomerID
            """,
            conn
        )

        conn.close()

        if customers.empty:

            st.info(
                "📦 No customers found."
            )

        else:

            st.dataframe(
                customers,
                use_container_width=True
            )

            st.success(
                f"✅ {len(customers)} customer(s) found."
            )

    # =====================================================
    # DELETE CUSTOMER
    # =====================================================

    with tab3:

        st.subheader("🗑️ Delete Customer")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT CustomerID, Name
            FROM customers
            ORDER BY CustomerID
            """
        )

        customers = cursor.fetchall()

        conn.close()

        if not customers:

            st.info(
                "📦 No customers available."
            )

        else:

            customer_options = {
                f"{customer_id} - {name}": customer_id
                for customer_id, name in customers
            }

            selected_customer = st.selectbox(
                "Select Customer",
                list(customer_options.keys()),
                key="delete_customer_select"
            )

            selected_id = customer_options[
                selected_customer
            ]

            confirm = st.checkbox(
                "I confirm that I want to delete this customer.",
                key="delete_customer_confirm"
            )

            if st.button(
                "🗑️ Delete Customer",
                key="delete_customer"
            ):

                if not confirm:

                    st.warning(
                        "⚠️ Please confirm before deleting."
                    )

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM customers
                        WHERE CustomerID = ?
                        """,
                        (selected_id,)
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        "✅ Customer deleted successfully!"
                    )

                    st.rerun()