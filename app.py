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

# Streamlit UI
def main():
    st.title("Inventory Management System")

    # Sidebar menu as a clean dropdown
    menu = ["Add Product", "View Products", "Alerts", "Export", "Barcode Scanner"]
    choice = st.sidebar.selectbox("Select an option", menu)

    elif choice == "Add Product":
        st.subheader("Add New Product")
    name = st.text_input("Product Name")
    barcode = st.text_input("Barcode")
    stock_level = st.number_input("Stock Level", min_value=0)

    # Replace with dropdowns
    reorder_level = st.selectbox("Reorder Level", [5, 10, 20, 50])
    price = st.selectbox("Price Range", [100.00, 250.00, 500.00, 1000.00])

    if st.button("Add"):
        db.add_product(name, barcode, stock_level, reorder_level, price)
        st.success(f"Added {name} successfully!")

    elif choice == "View Products":
        st.subheader("Product List")
        df = db.view_products()
        st.dataframe(df)

    elif choice == "Alerts":
        st.subheader("Stock Alerts")
    alerts_data = alerts.check_alerts()
    if alerts_data:
        df_alerts = pd.DataFrame(alerts_data, columns=["Product", "Stock Level", "Reorder Level"])
        st.table(df_alerts)
    else:
        st.success("No alerts. All stock levels are sufficient.")

    elif choice == "Export":
        st.subheader("Export Inventory")
        if st.button("Export to CSV"):
            filename = export.export_to_csv()
            st.success(f"Data exported to {filename}")

    elif choice == "Barcode Scanner":
        st.subheader("Find Product by Barcode")
        # Instead of typing, show dropdown of available barcodes
        df = db.view_products()
        if not df.empty:
            barcode_list = df['barcode'].dropna().tolist()
            selected_barcode = st.selectbox("Choose a barcode", barcode_list)
            if st.button("Search"):
                product = barcode_scanner.find_product_by_barcode(selected_barcode)
                if product:
                    st.write(product)
                else:
                    st.error("Product not found")
        else:
            st.info("No products available yet.")

     elif choice == "Delete Product":
        st.subheader("Delete Product")
    df = db.view_products()
    if not df.empty:
        product_names = df['name'].tolist()
        selected_product = st.selectbox("Choose product to delete", product_names)
        if st.button("Delete"):
            db.delete_product(selected_product)
            st.success(f"Deleted {selected_product} successfully!")
    else:
        st.info("No products available to delete.")

if __name__ == "__main__":
    db.init_db()
    main()