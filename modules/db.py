import sqlite3
import pandas as pd

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

def add_product(name, barcode, stock_level, reorder_level, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, barcode, stock_level, reorder_level, price) VALUES (?, ?, ?, ?, ?)",
              (name, barcode, stock_level, reorder_level, price))
    conn.commit()
    conn.close()

def view_products():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

# New functions below

def delete_product(name):
    """Delete a product by name"""
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE name=?", (name,))
    conn.commit()
    conn.close()

def find_product_by_name(name):
    """Find a product by name"""
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE name=?", (name,))
    product = c.fetchone()
    conn.close()
    return product