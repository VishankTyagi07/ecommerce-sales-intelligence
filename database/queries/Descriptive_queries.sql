/* 
Contains the Descriptive queries - What Happened?
Queries executed are:

General summaries
Time-based summaries
Top & bottom performers
Profitability

Author: Vishank
Created: 11 December 2025
*/

--General summaries

--total orders
SELECT COUNT(*) AS total_orders FROM cleaned_sales_data;

--total profit and total sales
SELECT SUM(sales) AS total_sales, SUM(profit) AS total_profit FROM cleaned_sales_data;

--sales of each category
SELECT product_category, SUM(sales) AS sales
FROM cleaned_sales_data
GROUP BY product_category
ORDER BY sales DESC;

--sales of each region
SELECT region, SUM(sales) AS sales
FROM cleaned_sales_data
GROUP BY region
ORDER BY sales DESC;

--Time-based summaries

--monthly sales
SELECT months AS month, SUM(sales) AS sales
FROM cleaned_sales_data
GROUP BY month
ORDER BY sales DESC;

--yearly sales
SELECT strftime('%Y', order_date) AS year, SUM(sales) AS sales
FROM cleaned_sales_data
GROUP BY year;

--Top & bottom performers

--Top 10 products
SELECT product, SUM(sales) AS total_sales
FROM cleaned_sales_data
GROUP BY product
ORDER BY total_sales DESC
LIMIT 10;

--Worst 10 products
SELECT product, SUM(sales) AS total_sales
FROM cleaned_sales_data
GROUP BY product
ORDER BY total_sales ASC
LIMIT 10;

--Top 10 customers
SELECT customer_name, SUM(sales) AS total_sales
FROM cleaned_sales_data
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;

--Profitability

--profit from each product
SELECT product, SUM(profit) AS profit
FROM cleaned_sales_data
GROUP BY product
ORDER BY profit DESC;

--customer segment and profit from each segments
SELECT segment, SUM(profit) AS segment_profit
FROM cleaned_sales_data
GROUP BY segment
ORDER BY segment_profit DESC;