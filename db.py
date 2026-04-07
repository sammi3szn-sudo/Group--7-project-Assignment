# modules/db.py
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "data", "inventory.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)
def init_db():
    conn = get_connection()
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
    def add_product(name, barcode, stock, reorder, price):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO products (name, barcode, stock_level, reorder_level, price) VALUES (?, ?, ?, ?, ?)",
              (name, barcode, stock, reorder, price))
    conn.commit()
    conn.close()