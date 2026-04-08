import sqlite3

def check_alerts():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT name, stock_level, reorder_level FROM products")
    alerts = []
    for name, stock, reorder in c.fetchall():
        if stock <= reorder:
            alerts.append(f"⚠️ {name} is low on stock ({stock} left)")
    conn.close()
    return alerts