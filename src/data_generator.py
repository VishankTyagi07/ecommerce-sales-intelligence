"""
E-Commerce Data Generator
Generates realistic fake data for the e-commerce analytics project

Tables Generated:
- customers.csv (1,000 records)
- products.csv (200 records)
- orders.csv (5,000 records)
- order_items.csv (15,000+ records)

Author: Vishank
Created: 9 December 2025
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)
Faker.seed(42)

# Ensure data/raw directory exists
os.makedirs('data/raw', exist_ok=True)

print("=" * 60)
print("E-COMMERCE DATA GENERATOR")
print("=" * 60)

# 1. GENERATE CUSTOMERS
def generate_customers(n=1000):
    """
    Generate customer data with demographics
    
    Args:
        n (int): Number of customers to generate
    
    Returns:
        pd.DataFrame: Customer data
    """
    print(f"\n Generating {n} customers...")
    
    customers = []
    
    for i in range(1, n + 1):
        # Generate age
        age = random.randint(18, 75)
        
        # Determine age category
        if age < 25:
            age_category = '18-24'
        elif age < 35:
            age_category = '25-34'
        elif age < 45:
            age_category = '35-44'
        elif age < 55:
            age_category = '45-54'
        else:
            age_category = '55+'
        
        # Registration date (between 3 years ago and today)
        registration_date = fake.date_between(start_date='-3y', end_date='today')
        
        customers.append({
            'customer_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'age': age,
            'age_category': age_category,
            'registration_date': registration_date,
            'city': fake.city(),
            'country': fake.country()
        })
    
    df = pd.DataFrame(customers)
    
    # Save to CSV
    df.to_csv('data/raw/customers.csv', index=False)
    print(f"   Saved to data/raw/customers.csv")
    print(f"   Records: {len(df)}")
    print(f"   Columns: {', '.join(df.columns)}")
    
    return df

# 2. GENERATE PRODUCTS
def generate_products(n=200):
    """
    Generate product catalog with brands and descriptions
    
    Args:
        n (int): Number of products to generate
    
    Returns:
        pd.DataFrame: Product data
    """
    print(f"\n Generating {n} products...")
    
    # Product categories and brands
    categories = {
        'Electronics': ['Samsung', 'Apple', 'Sony', 'LG', 'Dell'],
        'Clothing': ['Nike', 'Adidas', 'Zara', 'H&M', 'Levi\'s'],
        'Home & Garden': ['IKEA', 'HomeDepot', 'Wayfair', 'Target', 'Amazon Basics'],
        'Sports': ['Wilson', 'Spalding', 'Under Armour', 'Puma', 'Reebok'],
        'Books': ['Penguin', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Hachette']
    }
    
    products = []
    
    for i in range(1, n + 1):
        # Select category and brand
        category = random.choice(list(categories.keys()))
        brand = random.choice(categories[category])
        
        # Generate pricing (cost and selling price)
        cost = round(random.uniform(10, 500), 2)
        price = round(cost * random.uniform(1.3, 2.5), 2)  # 30-150% markup
        
        # Generate product name
        product_name = f"{brand} {fake.catch_phrase()}"
        
        # Generate description (varying lengths)
        if random.random() < 0.3:  # 30% short descriptions
            description = fake.sentence(nb_words=8)
        elif random.random() < 0.6:  # 30% medium
            description = fake.sentence(nb_words=20)
        else:  # 40% detailed
            description = ' '.join(fake.sentences(nb=3))
        
        products.append({
            'product_id': i,
            'product_name': product_name,
            'description': description,
            'category': category,
            'sub_category': fake.word(),
            'brand': brand,
            'price': price,
            'cost': cost,
            'stock_quantity': random.randint(0, 500)
        })
    
    df = pd.DataFrame(products)
    
    # Save to CSV
    df.to_csv('data/raw/products.csv', index=False)
    print(f"    Saved to data/raw/products.csv")
    print(f"    Records: {len(df)}")
    print(f"    Columns: {', '.join(df.columns)}")
    
    return df

# 3. GENERATE ORDERS
def generate_orders(customers_df, n=5000):
    """
    Generate order headers
    
    Args:
        customers_df (pd.DataFrame): Customer data
        n (int): Number of orders to generate
    
    Returns:
        pd.DataFrame: Order data
    """
    print(f"\n Generating {n} orders...")
    
    customer_ids = customers_df['customer_id'].tolist()
    registration_dates = dict(zip(customers_df['customer_id'], 
                                  customers_df['registration_date']))
    
    orders = []
    
    for i in range(1, n + 1):
        # Select random customer
        customer_id = random.choice(customer_ids)
        
        # Order date must be after customer registration
        reg_date = pd.to_datetime(registration_dates[customer_id])
        days_since_reg = (datetime.now() - reg_date).days
        
        if days_since_reg > 0:
            order_date = reg_date + timedelta(days=random.randint(0, days_since_reg))
        else:
            order_date = reg_date
        
        # Ship date (1-7 days after order)
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        
        # Return date (10-15% of orders are returned)
        return_date = None
        if random.random() < 0.12:  # 12% return rate
            # Returns happen 3-30 days after order
            return_date = order_date + timedelta(days=random.randint(3, 30))
        
        # Shipping mode
        ship_mode = random.choice(['Standard', 'Express', 'Same Day'])
        
        orders.append({
            'order_id': i,
            'customer_id': customer_id,
            'order_date': order_date.date(),
            'ship_date': ship_date.date(),
            'return_date': return_date.date() if return_date else None,
            'ship_mode': ship_mode,
            'total_amount': 0  # Will be calculated after order items
        })
    
    df = pd.DataFrame(orders)
    
    print(f"    Generated {len(df)} orders")
    
    return df

# 4. GENERATE ORDER ITEMS
def generate_order_items(orders_df, products_df):
    """
    Generate order line items (products in each order)
    
    Args:
        orders_df (pd.DataFrame): Order data
        products_df (pd.DataFrame): Product data
    
    Returns:
        tuple: (order_items_df, updated_orders_df)
    """
    print(f"\n Generating order items...")
    
    product_ids = products_df['product_id'].tolist()
    product_info = dict(zip(products_df['product_id'], 
                            zip(products_df['price'], products_df['cost'])))
    
    order_items = []
    order_totals = {}
    order_item_id = 1
    
    for order_id in orders_df['order_id']:
        # Each order has 1-5 items
        num_items = random.choices([1, 2, 3, 4, 5], 
                                   weights=[30, 35, 20, 10, 5])[0]
        
        order_total = 0
        selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
        
        for product_id in selected_products:
            price, cost = product_info[product_id]
            
            # Quantity (1-3 items of same product)
            quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            
            # Discount (0-30%)
            discount = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]), 2)
            
            # Calculations
            unit_price = price
            item_revenue = unit_price * quantity * (1 - discount)
            item_cost = cost * quantity
            profit = item_revenue - item_cost
            
            order_items.append({
                'order_item_id': order_item_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount': discount,
                'profit': round(profit, 2)
            })
            
            order_total += item_revenue
            order_item_id += 1
        
        order_totals[order_id] = round(order_total, 2)
    
    # Create DataFrame
    order_items_df = pd.DataFrame(order_items)
    
    # Update order totals
    orders_df['total_amount'] = orders_df['order_id'].map(order_totals)
    
    # Save to CSV
    order_items_df.to_csv('data/raw/order_items.csv', index=False)
    orders_df.to_csv('data/raw/orders.csv', index=False)
    
    print(f"    Saved to data/raw/order_items.csv")
    print(f"    Records: {len(order_items_df)}")
    print(f"    Updated data/raw/orders.csv with totals")
    
    return order_items_df, orders_df

# 5. GENERATE SUMMARY STATISTICS
def print_summary(customers_df, products_df, orders_df, order_items_df):
    """Print summary statistics of generated data"""
    
    
    print(" DATA GENERATION SUMMARY")

    
    print(f"\n CUSTOMERS:")
    print(f"   Total: {len(customers_df)}")
    print(f"   Countries: {customers_df['country'].nunique()}")
    print(f"   Age Range: {customers_df['age'].min()}-{customers_df['age'].max()}")
    print(f"   Age Distribution:")
    for cat in ['18-24', '25-34', '35-44', '45-54', '55+']:
        count = len(customers_df[customers_df['age_category'] == cat])
        pct = count * 100 / len(customers_df)
        print(f"      {cat}: {count} ({pct:.1f}%)")
    
    print(f"\n PRODUCTS:")
    print(f"   Total: {len(products_df)}")
    print(f"   Categories: {products_df['category'].nunique()}")
    print(f"   Brands: {products_df['brand'].nunique()}")
    print(f"   Price Range: ${products_df['price'].min():.2f} - ${products_df['price'].max():.2f}")
    print(f"   Category Distribution:")
    for cat in products_df['category'].value_counts().items():
        print(f"      {cat[0]}: {cat[1]}")
    
    print(f"\n ORDERS:")
    print(f"   Total: {len(orders_df)}")
    print(f"   Date Range: {orders_df['order_date'].min()} to {orders_df['order_date'].max()}")
    print(f"   Returned Orders: {orders_df['return_date'].notna().sum()} ({orders_df['return_date'].notna().sum() * 100 / len(orders_df):.1f}%)")
    print(f"   Total Revenue: ${orders_df['total_amount'].sum():,.2f}")
    print(f"   Average Order Value: ${orders_df['total_amount'].mean():.2f}")
    
    print(f"\n ORDER ITEMS:")
    print(f"   Total: {len(order_items_df)}")
    print(f"   Avg Items per Order: {len(order_items_df) / len(orders_df):.2f}")
    print(f"   Total Units Sold: {order_items_df['quantity'].sum():,}")
    print(f"   Total Profit: ${order_items_df['profit'].sum():,.2f}")
    
    
    print(" DATA GENERATION COMPLETE!")
    
    print("\n Files created in data/raw/:")
    print("   - customers.csv")
    print("   - products.csv")
    print("   - orders.csv")
    print("   - order_items.csv")
     
# MAIN EXECUTION
if __name__ == "__main__":
    try:
        # Generate all data
        customers = generate_customers(1000)
        products = generate_products(200)
        orders = generate_orders(customers, 5000)
        order_items, orders_updated = generate_order_items(orders, products)
        
        # Print summary
        print_summary(customers, products, orders_updated, order_items)
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        print("Data generation failed. Please check the error above.")