import sqlite3

def check_alerts():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT name, stock_level, reorder_level FROM products WHERE stock_level <= reorder_level")
    alerts = c.fetchall()
    conn.close()
    return alerts