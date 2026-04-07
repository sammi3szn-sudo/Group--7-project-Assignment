# barcode_scanner.py
import streamlit as st

class BarcodeScanner:
    """Manual barcode entry only (no pyzbar/Pillow needed)"""

    def __init__(self):
        self.pyzbar_available = False
            def scan_image(self, image_bytes):
        return None  # Image scanning disabled
        def render_ui(self):
        st.markdown("### 📷 Barcode Scanner (Manual Entry Only)")
        barcode_input = st.text_input("Enter barcode manually:", placeholder="e.g., 123456789012")
        barcode = None
        if st.button("Use Barcode"):
            barcode = barcode_input.strip() or None
        return barcode