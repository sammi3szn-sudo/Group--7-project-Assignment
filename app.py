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