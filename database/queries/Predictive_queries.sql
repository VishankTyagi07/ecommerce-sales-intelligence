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
SELECT 
CASE strftime('%m', order_date)
        WHEN '01' THEN 'January' WHEN '02' THEN 'February' WHEN '03' THEN 'March'
        WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June'
        WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October'
        WHEN '11' THEN 'November' WHEN '12' THEN 'December'
    END AS months, COUNT(order_id) AS orders, SUM(sales) AS sales
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
--low profit
SELECT *
FROM cleaned_sales_data
WHERE profit < 0
ORDER BY profit ASC;
--high aging
SELECT *
FROM cleaned_sales_data
WHERE aging > 10
ORDER BY aging DESC;