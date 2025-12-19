"""
This file generates Excel reports for e-commerce sales analysis.

It produces three Excel reports corresponding to:
1. Descriptive Analysis
2. Predictive Analysis
3. Prescriptive Analysis

Each report contains outputs from query functions
defined in the analytics module.

Author: Vishank Tyagi
Created: 11 December 2025
"""

# ========================
# Imports
# ========================
import os
import pandas as pd

from src.analytics import SalesAnalytics


# ========================
# Report Generator Class
# ========================
class ReportGenerator:
    def __init__(
        self,
        db_path: str = "database/ecommerce.db",
        report_path: str = "reports"
    ):
        """
        Initialize ReportGenerator with database and report paths.
        Paths are relative to project root for cloud compatibility.
        """
        self.analytics = SalesAnalytics()
        self.reports = report_path

        os.makedirs(self.reports, exist_ok=True)

    # ========================
    # Descriptive Reports
    # ========================
    def generate_descriptive_reports(self):
        try:
            descriptive_data = {
                "Total Orders": self.analytics.Count_Total_Orders(),
                "Profit Generated": self.analytics.Sales_generated_Profit(),
                "Categorical Sales": self.analytics.Categorical_Sales(),
                "Regional Sales": self.analytics.Regional_Sales(),
                "Monthly Sales": self.analytics.Monthly_Sales(),
                "Yearly Sales": self.analytics.Yearly_Sales(),
                "Profit Per Product": self.analytics.Products_profits(),
                "Profit Per Segment": self.analytics.Customer_Segments_Profit(),
                "Top Products": self.analytics.Best_Products(limit=10),
                "Worst Products": self.analytics.Worst_Products(limit=10),
                "Best Customers": self.analytics.Top_Customers(limit=10),
            }

            file_path = os.path.join(self.reports, "Descriptive_Analysis_Report.xlsx")

            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                for sheet_name, df in descriptive_data.items():
                    df.to_excel(writer, index=False, sheet_name=sheet_name[:31])

            return file_path

        except Exception as e:
            raise RuntimeError(f"Error generating descriptive report: {e}")

    # ========================
    # Predictive Reports
    # ========================
    def generate_predictive_reports(self):
        try:
            predictive_data = {
                "RFM Signals": self.analytics.RFM_signals(),
                "Seasonal Demands": self.analytics.Seasonal_demands(),
                "Product Performance Trends": self.analytics.Product_performance(),
                "Monthly Sales Forecasting": self.analytics.Monthly_sales_forecasting(),
                "High Risk Orders": self.analytics.High_risk_orders(),
            }

            file_path = os.path.join(self.reports, "Predictive_Analysis_Report.xlsx")

            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                for section_name, result in predictive_data.items():

                    if isinstance(result, pd.DataFrame):
                        result.to_excel(
                            writer,
                            index=False,
                            sheet_name=section_name[:31],
                        )

                    elif isinstance(result, dict):
                        for key, df in result.items():
                            sheet_name = f"{section_name[:15]}_{str(key)[:10]}"
                            df.to_excel(writer, index=False, sheet_name=sheet_name)

            return file_path

        except Exception as e:
            raise RuntimeError(f"Error generating predictive report: {e}")

    # ========================
    # Prescriptive Reports
    # ========================
    def generate_prescriptive_reports(self):
        try:
            prescriptive_data = {
                "Products to Discount": self.analytics.Products_to_Discount(),
                "Products to Promote": self.analytics.Products_to_promote(),
                "Customer Loyalty": self.analytics.Loyal_customers(),
                "Customer Churning": self.analytics.Churning_customers(),
                "Cities Needing Improvement": self.analytics.Cities_improvement(),
                "Optimized Shipping": self.analytics.Optimized_shipping(),
            }

            file_path = os.path.join(self.reports, "Prescriptive_Analysis_Report.xlsx")

            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                for sheet_name, df in prescriptive_data.items():
                    df.to_excel(writer, index=False, sheet_name=sheet_name[:31])

            return file_path

        except Exception as e:
            raise RuntimeError(f"Error generating prescriptive report: {e}")

    # ========================
    # Generate All Reports
    # ========================
    def generate_all_reports(self):
        self.generate_descriptive_reports()
        self.generate_predictive_reports()
        self.generate_prescriptive_reports()


# ========================
# Script Entry Point
# ========================
if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate_all_reports()
