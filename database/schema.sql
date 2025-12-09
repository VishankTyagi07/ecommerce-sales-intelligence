
-- E-COMMERCE DATABASE SCHEMA
-- Purpose: Define tables for sales analytics
-- Author: Vishank
-- Created:9 December 2025 


-- Drop existing tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS category;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER CHECK(age >= 18 AND age <= 120),
    age_category TEXT CHECK(age_category IN ('18-24', '25-34', '35-44', '45-54', '55+')),
    registration_date DATE NOT NULL,
    city TEXT,
    country TEXT
);

-- Index for faster lookups
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_customers_age_category ON customers(age_category);


CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    sub_category TEXT,
    brand TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    cost REAL NOT NULL CHECK(cost > 0),
    stock_quantity INTEGER DEFAULT 0 CHECK(stock_quantity >= 0)
);

-- Indexes for faster queries
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_price ON products(price);


CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    return_date DATE,
    ship_mode TEXT CHECK(ship_mode IN ('Standard', 'Express', 'Same Day')),
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    
    -- Foreign key constraint
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    -- Business rule: ship_date must be after order_date
    CHECK(ship_date IS NULL OR ship_date >= order_date),
    
    -- Business rule: return_date must be after order_date
    CHECK(return_date IS NULL OR return_date >= order_date)
);

-- Indexes for faster queries
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_return ON orders(return_date);


CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price > 0),
    discount REAL DEFAULT 0 CHECK(discount >= 0 AND discount <= 1),
    profit REAL,
    
    -- Foreign key constraints
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indexes for faster queries
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);


-- View: Order summary with customer info
CREATE VIEW v_order_summary AS
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount,
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.country,
    CASE WHEN o.return_date IS NOT NULL THEN 'Returned' ELSE 'Completed' END as order_status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- View: Product sales summary
CREATE VIEW v_product_sales AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(oi.order_item_id) as times_sold,
    SUM(oi.quantity) as total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) as total_revenue,
    ROUND(SUM(oi.profit), 2) as total_profit
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id;


-- Display table information
SELECT 'Schema created successfully!' as status;
SELECT 'Tables created:' as info;
SELECT name as table_name FROM sqlite_master WHERE type='table' ORDER BY name;
