import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.pdfgen import canvas


def billing():

    st.title("🛒 Billing System")

    # Check products.csv
    if not os.path.exists("products.csv"):
        st.error("products.csv not found.")
        return

    products = pd.read_csv("products.csv")

    if products.empty:
        st.warning("No products available.")
        return

    # Create sales.csv if it doesn't exist
    if not os.path.exists("sales.csv"):
        sales = pd.DataFrame(columns=[
            "Date",
            "Time",
            "Product",
            "Quantity",
            "Price",
            "Total"
        ])
        sales.to_csv("sales.csv", index=False)

    # Select Product
    product_name = st.selectbox(
        "Select Product",
        products["Product"]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Generate Bill"):

        product = products[
            products["Product"] == product_name
        ].iloc[0]

        price = float(product["Price"])
        stock = int(product["Stock"])

        # Check stock
        if quantity > stock:
            st.error("❌ Not enough stock available.")
            return

        total = price * quantity

        # Current Date & Time
        today = datetime.now()

        date = today.strftime("%d-%m-%Y")
        time = today.strftime("%H:%M:%S")

        # Update Stock
        products.loc[
            products["Product"] == product_name,
            "Stock"
        ] = stock - quantity

        products.to_csv(
            "products.csv",
            index=False
        )

        # Save Sale
        sales = pd.read_csv("sales.csv")

        new_sale = pd.DataFrame({

            "Date": [date],
            "Time": [time],
            "Product": [product_name],
            "Quantity": [quantity],
            "Price": [price],
            "Total": [total]

        })

        sales = pd.concat(
            [sales, new_sale],
            ignore_index=True
        )

        sales.to_csv(
            "sales.csv",
            index=False
        )

        # Generate PDF Receipt
        pdf = canvas.Canvas("receipt.pdf")

        pdf.setTitle("Receipt")

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(150, 800, "Grocery Store")

        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, 760, f"Date : {date}")
        pdf.drawString(50, 740, f"Time : {time}")

        pdf.drawString(50, 700, f"Product : {product_name}")
        pdf.drawString(50, 680, f"Quantity : {quantity}")
        pdf.drawString(50, 660, f"Price : ₹{price:.2f}")
        pdf.drawString(50, 640, f"Total : ₹{total:.2f}")

        pdf.drawString(50, 600, "Thank You For Shopping!")

        pdf.save()

        # Display Bill
        st.success("✅ Bill Generated Successfully!")

        st.subheader("Receipt")

        st.write("📅 Date :", date)
        st.write("🕒 Time :", time)
        st.write("🛒 Product :", product_name)
        st.write("📦 Quantity :", quantity)
        st.write("💵 Price :", f"₹{price:.2f}")
        st.write("💰 Total :", f"₹{total:.2f}")

        st.info("📄 receipt.pdf generated successfully.")

        # Download PDF
        with open("receipt.pdf", "rb") as pdf_file:
            st.download_button(
                label="⬇️ Download Receipt",
                data=pdf_file,
                file_name="receipt.pdf",
                mime="application/pdf"
            )