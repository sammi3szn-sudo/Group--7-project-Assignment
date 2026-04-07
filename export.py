# modules/export.py
from modules import db
import pandas as pd
def export_csv():
    products = db.get_products()
    if not products:
        return None
    df = pd.DataFrame(products, columns=["ID", "Name", "Barcode", "Stock", "Reorder Level", "Price"])
    return df