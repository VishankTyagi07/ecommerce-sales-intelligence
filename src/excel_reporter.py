"""
This File is generates excel reports,
There will be three excel reports which will show the three type of analysis on ecommerce data,
In the format of the excel spreadsheets.
These Three types of analysis will be:
1.Descriptive analysis
2.Predictive analysis
3.Prescriptive analysis

These three analysis will contain the query functions previousy made in analytics.py file

Author: Vishank
Created: 11 December 2025
"""
#import packages
import sys
sys.path.append("C:/Users/ASUS/Documents/ecommerce-sales-intelligence")
import os
import pandas as pd
from src.analytics import SalesAnalytics

class ReportGenerator:

    #path connection.
    def __init__(self, db_path="C:/Users/ASUS/Documents/ecommerce-sales-intelligence/database/ecommerce.db",
                 report_path="C:/Users/ASUS/Documents/ecommerce-sales-intelligence/reports"):
        self.analytics=SalesAnalytics(db_path=db_path)
        self.reports=report_path

        os.makedirs(self.reports,exist_ok=True)

    #Generating Descriptive Analysis
    def Generator_Descriptive_Reports(self):
        try:
            Descriptive_data = {
                "Total Orders":self.analytics.Count_Total_Orders(),
                "Profit Generated": self.analytics.Sales_generated_Profit(),
                "Categorical Sales":self.analytics.Categorical_Sales(),
                "Regional Sales":self.analytics.Regional_Sales(),
                "Monthly Sales":self.analytics.Monthly_Sales(),
                "Yearly Sales":self.analytics.Yearly_Sales(),
                "Profit Per Product":self.analytics.Products_profits(),
                "Profit Per Segment":self.analytics.Customer_Segments_Profit(),
                "Top Products":self.analytics.Best_Products(limit=10),
                "Worst Products":self.analytics.Worst_Products(limit=10),
                "Best Customers":self.analytics.Top_Customers(limit=10)
            }
            file_path=os.path.join(self.reports,"Descriptive_Analysis_reports.xlsx")

            with pd.ExcelWriter(file_path,engine="openpyxl") as writer:
                for sheet_name, df in Descriptive_data.items():
                    df.to_excel(writer,index=False,sheet_name=sheet_name[:31])
            print("The excel file for Descriptive analysis is generated")
            return file_path        
        except Exception as e:
            print("Error Generating Descriptive Report",e)

    def Generator_Predictive_Reports(self):
        try:
            Predictive_data = {
                "RFM Signals":self.analytics.RFM_signals(),
                "Seasonal Demands": self.analytics.Seasonal_demands(),
                "Products Performance Trends":self.analytics.Product_performance(),
                "Monthly Sales For Forecasting":self.analytics.Monthly_sales_forecasting(),
                "High risk orders":self.analytics.High_risk_orders()
            }
            file_path=os.path.join(self.reports,"Predictive_Analysis_reports.xlsx")

            with pd.ExcelWriter(file_path,engine="openpyxl") as writer:
                for section_name, df in Predictive_data.items():

                    #if the function have only one dataframe
                    if isinstance(df, pd.DataFrame):
                        safe_name = section_name[:31]
                        df.to_excel(writer, index=False, sheet_name=safe_name)

                    #if the function have multiple data frames and are present in a dictionary
                    elif isinstance(df,dict):
                        for key, df in df.items():
                            sheet_name = f"{section_name[:15]}_{str(key)[:10]}"
                            if isinstance(df, pd.DataFrame):
                                df.to_excel(writer, index=False, sheet_name=sheet_name)

                    else:
                        print(f"Skipping unsupported result type for: {section_name}")  

            print("The excel file for Predictive analysis is generated")
            return file_path        
        except Exception as e:
            print("Error Generating Predictive Report",e)

    def Generator_Prescriptive_Reports(self):
        try:
            Prescriptive_data = {
                "Products to discount":self.analytics.Products_to_Discount(),
                "Products to Promote": self.analytics.Products_to_promote(),
                "Customer Loyalty":self.analytics.Loyal_customers(),
                "Customer Churning":self.analytics.Churning_customers(),
                "Cities Needing Logistic Improving":self.analytics.Cities_improvement(),
                "Ship Modes To Improve":self.analytics.Optimized_shipping()
            }
            file_path=os.path.join(self.reports,"Prescriptive_Analysis_reports.xlsx")

            with pd.ExcelWriter(file_path,engine="openpyxl") as writer:
                for sheet_name, df in Prescriptive_data.items():
                    df.to_excel(writer,index=False,sheet_name=sheet_name[:31])
            print("The excel file for Prescriptive analysis is generated")
            return file_path        
        except Exception as e:
            print("Error Generating Prescriptive Report",e)    

    def generate_all_reports(self):
        print("Generate Descriptive report")
        self.Generator_Descriptive_Reports()
        print("Generate Predictive report")
        self.Generator_Predictive_Reports()
        print("Generate Prescriptive report")
        self.Generator_Prescriptive_Reports()

if __name__=="__main__":
    reportgenerator=ReportGenerator()
    reportgenerator.generate_all_reports()