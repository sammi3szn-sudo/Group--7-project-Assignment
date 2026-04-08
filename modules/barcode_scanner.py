import sqlite3

def find_product_by_barcode(barcode):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
    product = c.fetchone()
    conn.close()
    return product