import pandas as pd
import sqlite3

def export_to_csv():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    filename = "inventory.csv"
    df.to_csv(filename, index=False)
    conn.close()
    return filename

def export_to_excel():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    filename = "inventory.xlsx"
    df.to_excel(filename, index=False)
    conn.close()
    return filename