import sqlite3
import pandas as pd

def export_to_csv(filename="inventory_export.csv"):
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    df.to_csv(filename, index=False)
    conn.close()
    return filename