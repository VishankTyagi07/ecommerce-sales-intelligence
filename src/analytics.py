'''
This Analytics file is for using the sql queries,
making functions of those sql queries,
So that they can be used for accessing the queries in any file or code 
in future for further analysis.

The functions I plan on making are:

1.Descriptive queries(current data analysis)
-General summaries
-Time-based summaries
-Top & bottom performers
-Profitability

2.Predictive queries(predicting from the current data)
-RFM (Recency, Frequency, Monetary) signals
-Seasonal demand patterns
-Product performance trend
-Forecasting signals (moving averages)
-High-risk orders (low profit or high aging)

3.Prescriptive queries(understanding current data for future correction in services)
-Products to discount (low sales + low profit)
-Products to promote (high sales + high profit)
-Customers to target for loyalty program
-Customers at risk of churn(customers not using the services)
-Cities requiring logistics improvement
-Ship modes requiring optimization

Author: Vishank
Created: 11 December 2025
'''
import pandas as pd
import sqlite3
import os
from typing import Dict

class SalesAnalytics:
    #connecting the database
    def __init__(self, db_relative_path="database/ecommerce.db"):
        # Absolute path to project root
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.db_path = os.path.join(project_root, db_relative_path)

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Database not found at {self.db_path}"
            )

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

# functions for descriptive queries

#general summaries

    #for counting total orders
    def Count_Total_Orders(self)-> pd.DataFrame:
        query="""SELECT COUNT(*) AS total_orders FROM cleaned_sales_data;"""
        return pd.read_sql_query(query, self.conn)
    
    #for finding total profit along with total sales
    def Sales_generated_Profit(self)-> pd.DataFrame:
        query="""SELECT SUM(sales) AS total_sales, SUM(profit) AS total_profit FROM cleaned_sales_data;"""
        return pd.read_sql_query(query, self.conn)
    
    #sales of each category
    def Categorical_Sales(self)-> pd.DataFrame:
        query="""SELECT product_category, SUM(sales) AS sales
                FROM cleaned_sales_data
                GROUP BY product_category
                ORDER BY sales DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #sales of each region
    def Regional_Sales(self)-> pd.DataFrame:
        query="""SELECT region, SUM(sales) AS sales
            FROM cleaned_sales_data
            GROUP BY region
            ORDER BY sales DESC;"""
        return pd.read_sql_query(query, self.conn)
    
#Time-based summaries

    #monthly sales
    def Monthly_Sales(self)-> pd.DataFrame:
        query="""SELECT 
            CASE strftime('%m', order_date)
            WHEN '01' THEN 'January' WHEN '02' THEN 'February' WHEN '03' THEN 'March'
            WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June'
            WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October'
            WHEN '11' THEN 'November' WHEN '12' THEN 'December'
            END AS month,
            SUM(sales) AS sales
            FROM cleaned_sales_data
            GROUP BY strftime('%m', order_date)
            ORDER BY strftime('%m', order_date);"""
        return pd.read_sql_query(query, self.conn)
    
    #yearly sales
    def Yearly_Sales(self)-> pd.DataFrame:
        query="""SELECT strftime('%Y', order_date) AS year, SUM(sales) AS sales
                FROM cleaned_sales_data
                GROUP BY year;"""
        return pd.read_sql_query(query, self.conn)

#Top & bottom performer

    #Top products

    def Best_Products(self,limit:int)-> pd.DataFrame:
        query=f"""SELECT product, SUM(sales) AS total_sales
                FROM cleaned_sales_data
                GROUP BY product
                ORDER BY total_sales DESC
                LIMIT {limit}"""
        return pd.read_sql_query(query, self.conn)

    #worst products

    def Worst_Products(self,limit:int)-> pd.DataFrame:
        query=f"""SELECT product, SUM(sales) AS total_sales
                FROM cleaned_sales_data
                GROUP BY product
                ORDER BY total_sales ASC 
                LIMIT {limit}"""
        return pd.read_sql_query(query, self.conn)
    
    #Top customers

    def Top_Customers(self,limit:int)-> pd.DataFrame:
        query=f"""SELECT customer_name, SUM(sales) AS total_sales
                FROM cleaned_sales_data
                GROUP BY customer_name
                ORDER BY total_sales DESC
                LIMIT {limit}"""
        return pd.read_sql_query(query, self.conn)

#Profitability

    #profit from each product

    def Products_profits(self)-> pd.DataFrame:
        query="""SELECT product, SUM(profit) AS profit
                FROM cleaned_sales_data
                GROUP BY product
                ORDER BY profit DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #customer segment and profit from each segments

    def Customer_Segments_Profit(self)-> pd.DataFrame:
        query="""SELECT segment, SUM(profit) AS segment_profit
                FROM cleaned_sales_data
                GROUP BY segment
                ORDER BY segment_profit DESC;"""
        return pd.read_sql_query(query, self.conn)
        

#2. Predictive queries

    #RFM (Recency, Frequency, Monetary) signals

    def RFM_signals(self)-> Dict[str, pd.DataFrame]:

        Recency_q="""SELECT customer_id,
                        customer_name,
                        MAX(order_date) AS last_order_date
                    FROM cleaned_sales_data
                    GROUP BY customer_id;"""
        
        Frequency_q="""SELECT customer_id, COUNT(order_id) AS total_orders
                    FROM cleaned_sales_data
                    GROUP BY customer_id;"""

        Monetary_q="""SELECT customer_id, SUM(sales) AS total_sales
                    FROM cleaned_sales_data
                    GROUP BY customer_id;"""
        
        Recency=pd.read_sql_query(Recency_q, self.conn)
        Frequency=pd.read_sql_query(Frequency_q, self.conn)
        Monetary=pd.read_sql_query(Monetary_q, self.conn)

        return {
            'Recency': Recency,
            'Frequency':Frequency,
            'Monetary':Monetary
        }

    #Monthly sales for detecting seasonal demands

    def Seasonal_demands(self)-> pd.DataFrame:
        query="""SELECT 
            CASE strftime('%m', order_date)
            WHEN '01' THEN 'January' WHEN '02' THEN 'February' WHEN '03' THEN 'March'
            WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June'
            WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October'
            WHEN '11' THEN 'November' WHEN '12' THEN 'December'
            END AS months, COUNT(order_id) AS orders, SUM(sales) AS sales
            FROM cleaned_sales_data
            GROUP BY months
            ORDER BY sales DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Product performance trend

    def Product_performance(self)-> pd.DataFrame:
        query="""SELECT product,
                strftime('%Y-%m', order_date) AS month,
                SUM(sales) AS monthly_sales
                FROM cleaned_sales_data
                GROUP BY product, month
                ORDER BY product, month;"""
        return pd.read_sql_query(query, self.conn)
    
    #Forecasting signals (moving averages)

    def Monthly_sales_forecasting(self)-> pd.DataFrame:
        query="""SELECT
                strftime('%Y-%m', order_date) AS month,
                SUM(sales) AS monthly_sales
                FROM cleaned_sales_data
                GROUP BY month
                ORDER BY month;"""
        return pd.read_sql_query(query, self.conn)
    
    #High risk orders(low profit or high aging)
    def High_risk_orders(self)-> pd.DataFrame:

        Profit_q="""SELECT *
                    FROM cleaned_sales_data
                    WHERE profit < 0
                    ORDER BY profit ASC;"""
        
        Aging_q="""SELECT *
                FROM cleaned_sales_data
                WHERE aging > 10
                ORDER BY aging DESC;"""

        Profit=pd.read_sql_query(Profit_q, self.conn)
        Aging=pd.read_sql_query(Aging_q, self.conn)

        return {
            'L_Profit': Profit,
            'H_Aging':Aging,
        }
    
#3. Prescriptive queries

    #Products to discount (low sales + low profit)

    def Products_to_Discount(self)-> pd.DataFrame:
        query="""SELECT product,
                SUM(sales) AS sales,
                SUM(profit) AS profit
                FROM cleaned_sales_data
                GROUP BY product
                HAVING sales < 500 AND profit < 0
                ORDER BY sales ASC, profit ASC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Products to Promote (High sales + High profit)

    def Products_to_promote(self)-> pd.DataFrame:
        query="""SELECT product,
                SUM(sales) AS sales,
                SUM(profit) AS profit
                FROM cleaned_sales_data
                GROUP BY product
                HAVING sales > 5000 AND profit > 1000
                ORDER BY profit DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Customers to target for loyalty program

    def Loyal_customers(self)-> pd.DataFrame:
        query="""SELECT customer_id, customer_name,
                SUM(sales) AS total_sales,
                COUNT(order_id) AS total_orders
                FROM cleaned_sales_data
                GROUP BY customer_id
                HAVING total_sales > 5000 OR total_orders > 15
                ORDER BY total_sales DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Customers at risk of churn(leaving the services)

    def Churning_customers(self)-> pd.DataFrame:
        query="""SELECT customer_id, customer_name,
                MAX(order_date) AS last_order
                FROM cleaned_sales_data
                GROUP BY customer_id
                ORDER BY last_order ASC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Cities requiring logistics improvement

    def Cities_improvement(self)-> pd.DataFrame:
        query="""SELECT city,
                AVG(aging) AS avg_delivery_delay
                FROM cleaned_sales_data
                GROUP BY city
                ORDER BY avg_delivery_delay DESC;"""
        return pd.read_sql_query(query, self.conn)
    
    #Ship modes requiring optimization

    def Optimized_shipping(self)-> pd.DataFrame:
        query="""SELECT ship_mode,
                AVG(aging) AS avg_delivery_days,
                SUM(shipping_cost) AS total_cost
                FROM cleaned_sales_data
                GROUP BY ship_mode
                ORDER BY avg_delivery_days DESC;"""
        return pd.read_sql_query(query, self.conn)
    

if __name__ == "__main__":
    print("Queries Analyzed")