# barcode_scanner.py
import streamlit as st

class BarcodeScanner:
    """Manual barcode entry only (no pyzbar/Pillow needed)"""

    def __init__(self):
        self.pyzbar_available = False