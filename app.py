from modules import db, alerts, export, barcode_scanner
import streamlit as st
import sqlite3
import pandas as pd

# Initialize database
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT UNIQUE,
            stock_level INTEGER DEFAULT 0,
            reorder_level INTEGER DEFAULT 5,
            price REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a product
def add_product(name, barcode, stock_level, reorder_level, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, barcode, stock_level, reorder_level, price) VALUES (?, ?, ?, ?, ?)",
              (name, barcode, stock_level, reorder_level, price))
    conn.commit()
    conn.close()

# Function to view products
def view_products():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df



# Streamlit UI
def main():
    st.title("Inventory Management System")

    # Sidebar menu
    menu = ["Add Product", "View Products", "Alerts", "Export", "Barcode Scanner"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("Add New Product")
        name = st.text_input("Product Name")
        barcode = st.text_input("Barcode")
        stock_level = st.number_input("Stock Level", min_value=0)
        reorder_level = st.number_input("Reorder Level", min_value=0)
        price = st.number_input("Price", min_value=0.0, format="%.2f")

        if st.button("Add"):
            db.add_product(name, barcode, stock_level, reorder_level, price)
            st.success(f"Added {name} successfully!")

    elif choice == "View Products":
        st.subheader("Product List")
        df = db.view_products()
        st.dataframe(df)

    elif choice == "Alerts":
        st.subheader("Stock Alerts")
        for alert in alerts.check_alerts():
            st.warning(alert)

    elif choice == "Export":
        st.subheader("Export Inventory")
        if st.button("Export to CSV"):
            filename = export.export_to_csv()
            st.success(f"Data exported to {filename}")

    elif choice == "Barcode Scanner":
        st.subheader("Find Product by Barcode")
        barcode = st.text_input("Enter barcode")
        if st.button("Search"):
            product = barcode_scanner.find_product_by_barcode(barcode)
            if product:
                st.write(product)
            else:
                st.error("Product not found")

if __name__ == "__main__":
    db.init_db()
    main()