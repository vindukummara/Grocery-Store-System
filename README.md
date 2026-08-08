# 🛒 Grocery Store Management System

## 📌 Project Overview

The **Grocery Store Management System** is a Python and Streamlit-based web application designed to manage grocery store operations digitally.

The system provides product management, billing, stock monitoring, sales reporting, customer management, supplier management, login, logout, forgot-password functionality, and product image management.

---

## 🎯 Main Objective

The main objective of this project is to simplify grocery store management by providing a single web application for managing products, customers, suppliers, billing, sales, and inventory.

---

# 🚀 Features

### 🔐 Authentication
- Admin Login
- Logout
- Forgot Password
- Security Question
- Password Reset

### 🏪 Product Management
- Add Product
- View Products
- Update Product
- Delete Product
- Search Product
- Product Image Upload

### 🛒 Billing
- Select products
- Enter quantity
- Calculate total
- Update stock
- Generate sales records
- Generate PDF receipt

### 📦 Inventory Management
- Stock tracking
- Low-stock detection
- Product search
- Product update

### 📊 Sales Management
- Sales records
- Sales report
- Total sales analysis

### 👥 Customer Management
- Add customer
- View customer information
- Manage customer records

### 🚚 Supplier Management
- Add supplier
- View supplier information
- Manage supplier records

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application |
| Pandas | CSV data handling |
| ReportLab | PDF receipt generation |
| CSV | Data storage |
| HTML/CSS | Streamlit interface styling |

---

# 📁 Project Structure

```text
grocery_store_system/
│
├── app.py
│
├── login.py
├── logout.py
├── dashboard.py
│
├── add_product.py
├── view_products.py
├── update_product.py
├── delete_product.py
├── search_product.py
│
├── billing.py
├── low_stock.py
├── sales_report.py
│
├── customer.py
├── supplier.py
│
├── products.csv
├── sales.csv
├── customers.csv
├── suppliers.csv
│
├── receipt.pdf
│
├── images/
│   ├── rice.jpg
│   ├── wheat_flour.jpg
│   ├── sugar.jpg
│   ├── salt.jpg
│   ├── cooking_oil.jpg
│   ├── milk.jpg
│   ├── curd.jpg
│   ├── butter.jpg
│   ├── cheese.jpg
│   ├── white_bread.jpg
│   ├── brown_bread.jpg
│   ├── apple.jpg
│   ├── banana.jpg
│   ├── tomato.jpg
│   ├── shampoo.jpg
│   └── detergent.jpg
│
├── docs/
│   ├── System_Flowchart.png
│   ├── Data_Flow_Diagram.png
│   ├── Module_Diagram.png
│   └── Database_Diagram.png
│
├── requirements.txt
└── README.md
```

---

# 📄 Data Files

### products.csv

Stores product information:

```text
ProductID
Product
Category
Price
Stock
Image
```

### sales.csv

Stores sales and billing information.

### customers.csv

Stores customer information.

### suppliers.csv

Stores supplier information.

---

# 🖼️ Product Images

Product images are stored inside:

```text
images/
```

Example:

```text
images/rice.jpg
images/milk.jpg
images/bread.jpg
```

The image path is stored in `products.csv`.

---

# 📊 Project Modules

```text
Login
   ↓
Dashboard
   ↓
Product Management
   ├── Add Product
   ├── View Products
   ├── Update Product
   ├── Delete Product
   └── Search Product
           ↓
        Billing
           ↓
       Sales Report
           ↓
      Low Stock Alert
```

Customer and Supplier Management are also available from the main application.

---

# 🔐 Login Details

### Default Username

```text
admin
```

### Default Password

```text
admin123
```

### Forgot Password

Click:

```text
🔑 Forgot Password?
```

Security question:

```text
What is your favourite color?
```

Default answer:

```text
blue
```

---

# ⚙️ Installation

## Step 1: Open Project

Open the project folder in **VS Code**.

```text
grocery_store_system
```

## Step 2: Open Terminal

In VS Code:

```text
Terminal → New Terminal
```

## Step 3: Install Requirements

Run:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install streamlit pandas reportlab
```

---

# ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# 🧪 Testing

Test the following modules after login:

```text
✅ Login
✅ Forgot Password
✅ Dashboard
✅ Add Product
✅ View Products
✅ Update Product
✅ Delete Product
✅ Search Product
✅ Billing
✅ Low Stock
✅ Sales Report
✅ Customer Management
✅ Supplier Management
✅ Logout
```

---

# 🧾 Billing Process

```text
Select Product
      ↓
Enter Quantity
      ↓
Calculate Price
      ↓
Calculate Total
      ↓
Update Stock
      ↓
Save Sale
      ↓
Generate Receipt
```

The sales information is stored in:

```text
sales.csv
```

The receipt is generated as:

```text
receipt.pdf
```

---

# 📉 Low Stock Management

The system checks available product stock and identifies products with low inventory.

This helps the store administrator know which products need to be restocked.

---

# 📊 Sales Report

The Sales Report module provides information about:

- Sales
- Products sold
- Quantity
- Total amount
- Sales history

---

# 📚 Documentation

Project diagrams are available inside:

```text
docs/
```

### System Flowchart

```text
docs/System_Flowchart.png
```

### Data Flow Diagram

```text
docs/Data_Flow_Diagram.png
```

### Module Diagram

```text
docs/Module_Diagram.png
```

### Database Diagram

```text
docs/Database_Diagram.png
```

---

# 🔮 Future Enhancements

The project can be enhanced with:

- SQLite / MySQL database
- Multiple user roles
- Admin and employee accounts
- Barcode scanner
- Online payment
- Email receipt
- WhatsApp receipt
- Cloud database
- Advanced sales analytics
- Inventory forecasting
- Customer purchase history
- Supplier purchase management

---

# 👨‍💻 Developer

**Name:** __________________________

**Project:** Grocery Store Management System

**Technology:** Python + Streamlit

**Purpose:** Educational / Academic Project

---

# 📜 License

This project is developed for educational and learning purposes.