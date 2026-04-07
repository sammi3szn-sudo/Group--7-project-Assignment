import sqlite3

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    barcode TEXT UNIQUE,
                    stock_level INTEGER DEFAULT 0,
                    reorder_level INTEGER DEFAULT 5,
                    price REAL DEFAULT 0.0
                )''')
    conn.commit()
    conn.close()

    def add_product(name, barcode, stock, reorder, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, barcode, stock_level, reorder_level, price) VALUES (?, ?, ?, ?, ?)",
              (name, barcode, stock, reorder, price))
    conn.commit()
    conn.close()
    def update_stock(barcode, qty):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("UPDATE products SET stock_level = stock_level + ? WHERE barcode = ?", (qty, barcode))
    conn.commit()
    conn.close()
    import pandas as pd
def get_products():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df
import streamlit as st

# --- Streamlit UI ---
st.title("📦 Inventory Management System")

# Confirm Streamlit works
st.write("✅ Streamlit is running correctly!")

# Initialize DB
init_db()

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Product", "Update Stock", "Reports"])
if menu == "Dashboard":
    st.subheader("Current Inventory")
    df = get_products()
    st.dataframe(df)
    elif menu == "Add Product":
    st.subheader("Add New Product")
    name = st.text_input("Product Name")
    barcode = st.text_input("Barcode")
    stock = st.number_input("Initial Stock", min_value=0)
    reorder = st.number_input("Reorder Level", min_value=0)
    price = st.number_input("Price", min_value=0.0)
    if st.button("Add Product"):
        add_product(name, barcode, stock, reorder, price)
        st.success("Product added successfully!")