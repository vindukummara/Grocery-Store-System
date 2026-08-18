import streamlit as st
import pandas as pd

from database import get_connection


def supplier():

    st.header("🚚 Supplier Management")

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Supplier",
            "📋 View Suppliers",
            "🗑️ Delete Supplier"
        ]
    )

    # =====================================================
    # ADD SUPPLIER
    # =====================================================

    with tab1:

        st.subheader("➕ Add Supplier")

        supplier_id = st.number_input(
            "Supplier ID",
            min_value=1,
            step=1
        )

        supplier_name = st.text_input(
            "Supplier Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        address = st.text_area(
            "Address"
        )

        if st.button(
            "➕ Add Supplier",
            key="add_supplier"
        ):

            if supplier_name.strip() == "":
                st.warning(
                    "⚠️ Please enter supplier name."
                )

                return

            conn = get_connection()
            cursor = conn.cursor()

            # Check Supplier ID
            cursor.execute(
                """
                SELECT SupplierID
                FROM suppliers
                WHERE SupplierID = ?
                """,
                (supplier_id,)
            )

            existing_supplier = cursor.fetchone()

            if existing_supplier:

                st.error(
                    "❌ Supplier ID already exists."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO suppliers
                    (
                        SupplierID,
                        SupplierName,
                        Phone,
                        Address
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        supplier_id,
                        supplier_name,
                        phone,
                        address
                    )
                )

                conn.commit()

                st.success(
                    "✅ Supplier added successfully!"
                )

            conn.close()

    # =====================================================
    # VIEW SUPPLIERS
    # =====================================================

    with tab2:

        st.subheader("📋 Supplier List")

        conn = get_connection()

        suppliers = pd.read_sql_query(
            """
            SELECT
                SupplierID,
                SupplierName,
                Phone,
                Address
            FROM suppliers
            ORDER BY SupplierID
            """,
            conn
        )

        conn.close()

        if suppliers.empty:

            st.info(
                "📦 No suppliers found."
            )

        else:

            st.dataframe(
                suppliers,
                use_container_width=True
            )

            st.success(
                f"✅ {len(suppliers)} supplier(s) found."
            )

    # =====================================================
    # DELETE SUPPLIER
    # =====================================================

    with tab3:

        st.subheader("🗑️ Delete Supplier")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT SupplierID, SupplierName
            FROM suppliers
            ORDER BY SupplierID
            """
        )

        suppliers = cursor.fetchall()

        conn.close()

        if not suppliers:

            st.info(
                "📦 No suppliers available."
            )

        else:

            supplier_options = {
                f"{supplier_id} - {supplier_name}": supplier_id
                for supplier_id, supplier_name in suppliers
            }

            selected_supplier = st.selectbox(
                "Select Supplier",
                list(supplier_options.keys()),
                key="delete_supplier_select"
            )

            selected_id = supplier_options[
                selected_supplier
            ]

            confirm = st.checkbox(
                "I confirm that I want to delete this supplier.",
                key="delete_supplier_confirm"
            )

            if st.button(
                "🗑️ Delete Supplier",
                key="delete_supplier"
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
                        DELETE FROM suppliers
                        WHERE SupplierID = ?
                        """,
                        (selected_id,)
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        "✅ Supplier deleted successfully!"
                    )

                    st.rerun()