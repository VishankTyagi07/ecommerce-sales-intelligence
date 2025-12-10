/* 
Contains the Prescriptive queries - What to do?
Queries executed are:

Products to discount (low sales + low profit)
Products to promote (high sales + high profit)
Customers to target for loyalty program
Customers at risk of churn
Cities requiring logistics improvement
Ship modes requiring optimization

Author: Vishank
Created: 11 December 2025
*/

--Products to discount (low sales + low profit)

SELECT product,
       SUM(sales) AS sales,
       SUM(profit) AS profit
FROM cleaned_sales_data
GROUP BY product
HAVING sales < 500 AND profit < 0
ORDER BY sales ASC, profit ASC;

--Products to promote (high sales + high profit)

SELECT product,
       SUM(sales) AS sales,
       SUM(profit) AS profit
FROM cleaned_sales_data
GROUP BY product
HAVING sales > 5000 AND profit > 1000
ORDER BY profit DESC;

--Customers to target for loyalty program

SELECT customer_id, customer_name,
       SUM(sales) AS total_sales,
       COUNT(order_id) AS total_orders
FROM cleaned_sales_data
GROUP BY customer_id
HAVING total_sales > 5000 OR total_orders > 15
ORDER BY total_sales DESC;

--Customers at risk of churn

SELECT customer_id, customer_name,
       MAX(order_date) AS last_order
FROM cleaned_sales_data
GROUP BY customer_id
ORDER BY last_order ASC;

--Cities requiring logistics improvement

SELECT city,
       AVG(aging) AS avg_delivery_delay
FROM cleaned_sales_data
GROUP BY city
ORDER BY avg_delivery_delay DESC;

--Ship modes requiring optimization

SELECT ship_mode,
       AVG(aging) AS avg_delivery_days,
       SUM(shipping_cost) AS total_cost
FROM cleaned_sales_data
GROUP BY ship_mode
ORDER BY avg_delivery_days DESC;