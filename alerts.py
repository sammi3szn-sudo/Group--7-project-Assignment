def show_low_stock_alerts():
    products = db.get_products()
    low_stock = [p for p in products if p[3] <= p[4]]  # stock_level <= reorder_level
    if low_stock:
        st.warning("⚠️ Low stock alerts:")
        for p in low_stock:
            st.write(f"{p[1]} (Stock: {p[3]}, Reorder Level: {p[4]})")