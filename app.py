from modules import db, alerts, export, barcode_scanner
import streamlit as st
import pandas as pd

def main():
    st.title("Inventory Management System")

    menu = ["Dashboard", "Add Product", "View Products", "Alerts", "Export", "Barcode Scanner", "Delete Product", "Search Product"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add Product":
        st.subheader("Add New Product")
        name = st.text_input("Product Name")
        barcode = st.text_input("Barcode")
        stock_level = st.number_input("Stock Level", min_value=0)
        reorder_level = st.selectbox("Reorder Level", [5, 10, 20, 50])
        price = st.selectbox("Price Range", [100.00, 250.00, 500.00, 1000.00])

        if st.button("Add"):
            db.add_product(name, barcode, stock_level, reorder_level, price)
            st.success(f"Added {name} successfully!")
    elif choice == "Dashboard":
        st.subheader("📊 Inventory Dashboard")

        df = db.view_products()

        if not df.empty:

            # --- METRICS ---
            total_products = len(df)
            total_stock = df["stock_level"].sum()
            low_stock = len(df[df["stock_level"] <= df["reorder_level"]])
            total_value = (df["stock_level"] * df["price"]).sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Products", total_products)
            col2.metric("Total Stock", total_stock)
            col3.metric("Low Stock Items", low_stock)
            col4.metric("Inventory Value", f"₦{total_value:,.2f}")

            st.divider()

            # --- STOCK LEVEL CHART ---
            st.write("### 📦 Stock Levels per Product")
            st.bar_chart(df.set_index("name")["stock_level"])

            # --- PRICE DISTRIBUTION ---
            st.write("### 💰 Price Distribution")
            st.bar_chart(df.set_index("name")["price"])

            # --- LOW STOCK TABLE ---
            st.write("### ⚠️ Low Stock Products")
            low_stock_df = df[df["stock_level"] <= df["reorder_level"]]

            if not low_stock_df.empty:
                st.dataframe(low_stock_df)
            else:
                st.success("No low stock items 🎉")

        else:
            st.info("No data available yet. Add some products first.")

    elif choice == "View Products":
        st.subheader("Product List")
        df = db.view_products()
        st.dataframe(df)

    elif choice == "Alerts":
        st.subheader("Stock Alerts")
        alerts_data = alerts.check_alerts()
        if alerts_data:
            df_alerts = pd.DataFrame(alerts_data, columns=["Product", "Stock Level", "Reorder Level"])
            st.table(df_alerts)
        else:
            st.success("No alerts. All stock levels are sufficient.")

    elif choice == "Export":
        st.subheader("Export Inventory")
        if st.button("Export to CSV"):
            filename = export.export_to_csv()
            st.success(f"Data exported to {filename}")
        if st.button("Export to Excel"):
            filename = export.export_to_excel()
            st.success(f"Data exported to {filename}")

    elif choice == "Barcode Scanner":
        st.subheader("Find Product by Barcode")
        df = db.view_products()
        if not df.empty:
            barcode_list = df['barcode'].dropna().tolist()
            selected_barcode = st.selectbox("Choose a barcode", barcode_list)
            if st.button("Search"):
                product = barcode_scanner.find_product_by_barcode(selected_barcode)
                if product:
                    st.write(product)
                else:
                    st.error("Product not found")
        else:
            st.info("No products available yet.")

    elif choice == "Delete Product":
        st.subheader("Delete Product")
        df = db.view_products()
        if not df.empty:
            product_names = df['name'].tolist()
            selected_product = st.selectbox("Choose product to delete", product_names)
            if st.button("Delete"):
                db.delete_product(selected_product)
                st.success(f"Deleted {selected_product} successfully!")
        else:
            st.info("No products available to delete.")

    elif choice == "Search Product":
        st.subheader("Find Product by Name")
        df = db.view_products()
        if not df.empty:
            product_names = df['name'].tolist()
            selected_name = st.selectbox("Choose a product", product_names)
            if st.button("Search"):
                product = db.find_product_by_name(selected_name)
                if product:
                    st.write(product)
                else:
                    st.error("Product not found")
        else:
            st.info("No products available yet.")

if __name__ == "__main__":
    db.init_db()
    main()