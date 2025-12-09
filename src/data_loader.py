"""
Data Loader
Loads CSV files into SQLite database

Author: Vishank
Created: 9 December 2025
"""

import pandas as pd
import sqlite3
import os

def load_data_to_database():
    """
    Load all CSV files into database tables
    """
    print("DATA LOADING PROCESS")
    
    db_path = 'database/ecommerce.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"\n ERROR: Database not found at {db_path}")
        print("   Please run 'python src/create_database.py' first!")
        return False
    
    # Check if CSV files exist
    csv_files = {
        'customers': 'data/raw/customers.csv',
        'products': 'data/raw/products.csv',
        'orders': 'data/raw/orders.csv',
        'order_items': 'data/raw/order_items.csv'
    }
    
    for table, path in csv_files.items():
        if not os.path.exists(path):
            print(f"\n ERROR: {path} not found!")
            print("   Please run 'python src/data_generator.py' first!")
            return False
    
    try:
        # Connect to database
        print(f"\n Connecting to database...")
        conn = sqlite3.connect(db_path)
        print("    Connected successfully")
        
        # Load each CSV file
        print(f"\n Loading data from CSV files...")
        
        # 1. Load Customers
        print(f"\n Loading customers...")
        customers = pd.read_csv(csv_files['customers'])
        customers.to_sql('customers', conn, if_exists='replace', index=False)
        print(f"    Loaded {len(customers)} customers")
        
        # 2. Load Products
        print(f"\n Loading products...")
        products = pd.read_csv(csv_files['products'])
        products.to_sql('products', conn, if_exists='replace', index=False)
        print(f"    Loaded {len(products)} products")
        
        # 3. Load Orders
        print(f"\n Loading orders...")
        orders = pd.read_csv(csv_files['orders'])
        orders.to_sql('orders', conn, if_exists='replace', index=False)
        print(f"    Loaded {len(orders)} orders")
        
        # 4. Load Order Items
        print(f"\n Loading order items...")
        order_items = pd.read_csv(csv_files['order_items'])
        order_items.to_sql('order_items', conn, if_exists='replace', index=False)
        print(f"    Loaded {len(order_items)} order items")
        
        # Verify data loaded
        print(f"\n All data loaded successfully!")
        print(f"\n VERIFICATION:")
        
        cursor = conn.cursor()
        
        # Check row counts
        tables = ['customers', 'products', 'orders', 'order_items']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count:,} rows")
        
        # Sample queries to verify data quality
        print(f"\n DATA QUALITY CHECKS:")
        
        # Check for null customer IDs in orders
        cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id IS NULL")
        null_customers = cursor.fetchone()[0]
        print(f"   Orders with null customer_id: {null_customers} {' if null_customers == 0 else '}")
        
        # Check for negative prices
        cursor.execute("SELECT COUNT(*) FROM products WHERE price < 0")
        neg_prices = cursor.fetchone()[0]
        print(f"   Products with negative price: {neg_prices} {'if neg_prices == 0 else' }")
        
        # Check total revenue
        cursor.execute("SELECT ROUND(SUM(total_amount), 2) FROM orders WHERE return_date IS NULL")
        total_revenue = cursor.fetchone()[0]
        print(f"   Total revenue (non-returned): ${total_revenue:,.2f} ")
        
        # Check return rate
        cursor.execute("""
            SELECT 
                ROUND(COUNT(CASE WHEN return_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) 
            FROM orders
        """)
        return_rate = cursor.fetchone()[0]
        print(f"   Return rate: {return_rate}% ")
        
        # Close connection
        conn.close()
        
        print(" DATA LOADING COMPLETE!")
        print(f"\n Database ready at: {db_path}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n Database Error: {e}")
        return False
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    load_data_to_database()