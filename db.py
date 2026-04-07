# modules/db.py
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "data", "inventory.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)