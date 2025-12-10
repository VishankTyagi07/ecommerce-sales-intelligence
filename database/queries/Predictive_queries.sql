/* 
Contains the Descriptive queries - What Happened?
Queries executed are:

RFM (Recency, Frequency, Monetary) signals
Seasonal demand patterns
Product performance trend
Forecasting signals (moving averages)
High-risk orders (low profit or high aging)

Author: Vishank
Created: 11 December 2025
*/

--RFM (Recency, Frequency, Monetary) signals

--Recency (days since last order per customer)

SELECT customer_id,
       customer_name,
       MAX(order_date) AS last_order_date
FROM cleaned_sales_data
GROUP BY customer_id;

--Frequency

SELECT customer_id, COUNT(order_id) AS total_orders
FROM cleaned_sales_data
GROUP BY customer_id;

--Monetary

SELECT customer_id, SUM(sales) AS total_sales
FROM cleaned_sales_data
GROUP BY customer_id;

--Seasonal demand patterns
SELECT months, COUNT(order_id) AS orders, SUM(sales) AS sales
FROM cleaned_sales_data
GROUP BY months
ORDER BY sales DESC;

--Product performance trend
SELECT product,
       strftime('%Y-%m', order_date) AS month,
       SUM(sales) AS monthly_sales
FROM cleaned_sales_data
GROUP BY product, month
ORDER BY product, month;

--Forecasting signals (moving averages)
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(sales) AS monthly_sales
FROM cleaned_sales_data
GROUP BY month
ORDER BY month;

--High-risk orders (low profit or high aging)
SELECT *
FROM cleaned_sales_data
WHERE profit < 0
ORDER BY profit ASC;

SELECT *
FROM cleaned_sales_data
WHERE aging > 10
ORDER BY aging DESC;