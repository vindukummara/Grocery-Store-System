import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas

from database import get_connection


def billing():

    st.header("🛒 Billing")

    # =====================================================
    # GET PRODUCTS FROM SQLITE
    # =====================================================

    conn = get_connection()

    products = pd.read_sql_query(
        """
        SELECT
            ProductID,
            Product,
            Price,
            Stock
        FROM products
        WHERE Stock > 0
        ORDER BY Product
        """,
        conn
    )

    conn.close()

    if products.empty:
        st.warning("⚠️ No products available for billing.")
        return

    # =====================================================
    # SELECT PRODUCT
    # =====================================================

    product_names = products["Product"].tolist()

    selected_product = st.selectbox(
        "Select Product",
        product_names
    )

    selected_row = products[
        products["Product"] == selected_product
    ].iloc[0]

    product_id = int(selected_row["ProductID"])
    price = float(selected_row["Price"])
    available_stock = int(selected_row["Stock"])

    st.write(f"**Price:** ₹{price:.2f}")
    st.write(f"**Available Stock:** {available_stock}")

    # =====================================================
    # QUANTITY
    # =====================================================

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=available_stock,
        value=1,
        step=1
    )

    total = price * quantity

    st.subheader(f"💰 Total: ₹{total:.2f}")

    # =====================================================
    # CREATE BILL
    # =====================================================

    if st.button("🧾 Generate Bill"):

        # -----------------------------
        # Check Stock Again
        # -----------------------------

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT Stock, Price, Product
            FROM products
            WHERE ProductID = ?
            """,
            (product_id,)
        )

        current_product = cursor.fetchone()

        if current_product is None:

            conn.close()

            st.error("❌ Product not found.")
            return

        current_stock = int(current_product[0])
        current_price = float(current_product[1])
        current_name = current_product[2]

        if quantity > current_stock:

            conn.close()

            st.error(
                f"❌ Only {current_stock} item(s) available."
            )
            return

        # =================================================
        # UPDATE STOCK
        # =================================================

        new_stock = current_stock - quantity

        cursor.execute(
            """
            UPDATE products
            SET Stock = ?
            WHERE ProductID = ?
            """,
            (
                new_stock,
                product_id
            )
        )

        # =================================================
        # SAVE SALE
        # =================================================

        now = datetime.now()

        sale_date = now.strftime("%Y-%m-%d")
        sale_time = now.strftime("%H:%M:%S")

        sale_total = current_price * quantity

        cursor.execute(
            """
            INSERT INTO sales
            (
                Date,
                Time,
                ProductID,
                Quantity,
                Price,
                Total
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                sale_date,
                sale_time,
                product_id,
                quantity,
                current_price,
                sale_total
            )
        )

        conn.commit()

        conn.close()

        # =================================================
        # GENERATE PDF RECEIPT
        # =================================================

        receipt_file = "receipt.pdf"

        pdf = canvas.Canvas(receipt_file)

        pdf.setTitle("Grocery Store Receipt")

        pdf.setFont("Helvetica-Bold", 18)

        pdf.drawString(
            180,
            800,
            "GROCERY STORE"
        )

        pdf.setFont("Helvetica", 11)

        pdf.drawString(
            50,
            770,
            f"Date: {sale_date}"
        )

        pdf.drawString(
            400,
            770,
            f"Time: {sale_time}"
        )

        pdf.line(
            50,
            750,
            550,
            750
        )

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            50,
            720,
            "Product"
        )

        pdf.drawString(
            300,
            720,
            "Quantity"
        )

        pdf.drawString(
            400,
            720,
            "Price"
        )

        pdf.drawString(
            480,
            720,
            "Total"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            50,
            690,
            str(current_name)
        )

        pdf.drawString(
            300,
            690,
            str(quantity)
        )

        pdf.drawString(
            400,
            690,
            f"₹{current_price:.2f}"
        )

        pdf.drawString(
            480,
            690,
            f"₹{sale_total:.2f}"
        )

        pdf.line(
            50,
            660,
            550,
            660
        )

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            380,
            630,
            f"Total: ₹{sale_total:.2f}"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            200,
            580,
            "Thank you for shopping with us!"
        )

        pdf.save()

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.success(
            "✅ Bill generated successfully!"
        )

        st.info(
            f"📦 Remaining stock: {new_stock}"
        )

        st.download_button(
            label="📥 Download Receipt",
            data=open(
                receipt_file,
                "rb"
            ).read(),
            file_name="receipt.pdf",
            mime="application/pdf"
        )