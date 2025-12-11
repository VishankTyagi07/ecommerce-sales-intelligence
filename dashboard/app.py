"""
This File Generates a Streamlit Dashboard Interface,
This interface helps  the user for analyzing the data using plots and dataframes,
without performing any type of programming

Author:Vishank
Created: 11 December 2025
"""

#importing packages
import sys
sys.path.append("C:/Users/ASUS/Documents/ecommerce-sales-intelligence")
import pandas as pd 
from src.analytics import SalesAnalytics
import plotly.express as px
import streamlit as st

#Title of the dashboard
st.set_page_config(layout="wide")
st.title("E-COMMERCE SALES DATA ANALYSIS")
st.sidebar.title("Types of Analysis That Can Be Performed On The Data")
#Calling SalesAnalytics class
analytics=SalesAnalytics("C:/Users/ASUS/Documents/ecommerce-sales-intelligence/database/ecommerce.db")
#Descriptive analysis Functions
Total_orders=analytics.Count_Total_Orders()

def auto_plot(df: pd.DataFrame):
    """Automatically generates a Plotly figure from any DataFrame."""
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    # Case 1: No numeric column → return empty figure with message
    if len(numeric_cols) == 0:
        fig = px.scatter(title="No numeric columns available to plot")
        return fig
    # Choose y axis (first numeric column)
    y = numeric_cols[0]
    # Case 2: No categorical column → use index as x
    if len(categorical_cols) == 0:
        x = df.index
        fig = px.line(df, x=x, y=y, title=f"{y} over index")
        return fig
    # Choose x axis (first non-numeric column)
    x = categorical_cols[0]
    # Plot auto figure
    fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")
    return fig


#Sidebar Analysis Options
Type_analysis=st.sidebar.radio("Pick a Type of Analysis",['Unselected','Descriptive Analysis','Predictive Analysis','Prescriptive Analysis'])

if Type_analysis=='Unselected':
    st.sidebar.write("**Select a Type of Analysis**")

elif Type_analysis =='Descriptive Analysis':
    st.sidebar.header("Descriptive Analysis Functions")
    st.sidebar.write("What do you want to analyze?")
    
    analysis_functions = {
        "Unselected":None,
        "Total Orders":analytics.Count_Total_Orders,
        "Profit Generated": analytics.Sales_generated_Profit,
        "Categorical Sales":analytics.Categorical_Sales,
        "Regional Sales":analytics.Regional_Sales,
        "Monthly Sales":analytics.Monthly_Sales,
        "Yearly Sales":analytics.Yearly_Sales,
        "Profit Per Product":analytics.Products_profits,
        "Profit Per Segment":analytics.Customer_Segments_Profit,
        "Top Products":analytics.Best_Products,
        "Worst Products":analytics.Worst_Products,
        "Best Customers":analytics.Top_Customers
    }
    choice = st.sidebar.selectbox("Choose analysis", analysis_functions.keys())
    func = analysis_functions[choice]
    if func:
        if func.__code__.co_argcount > 1:    # function has parameters
            param = st.sidebar.number_input("Enter parameter value:", value=5)
            if st.sidebar.button("Show"):

                df = func(param)
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)
        else:                                # no-parameter function
            if st.sidebar.button("Show"):

                df = func()
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)

elif Type_analysis =='Predictive Analysis':
    st.sidebar.header("Predictive Analysis Functions")
    st.sidebar.write("What do you want to analyze?")
    
    analysis_functions = {
        "Unselected":None,
        "RFM Signals":analytics.RFM_signals,
        "Seasonal Demands": analytics.Seasonal_demands,
        "Products Performance Trends":analytics.Product_performance,
        "Monthly Sales For Forecasting":analytics.Monthly_sales_forecasting,
        "High risk orders":analytics.High_risk_orders
    }
    choice = st.sidebar.selectbox("Choose analysis", analysis_functions.keys())
    func = analysis_functions[choice]
    if func:
        if choice == "RFM Signals":
            if st.sidebar.button("Show RFM Signals"):
                rfm_dict = func()   # returns { "RFM":df1 , "Scores":df2 , ... }

                for name, df in rfm_dict.items():
                    st.subheader(name)  

                    fig = auto_plot(df)
                    st.plotly_chart(fig,width='stretch') 

                    st.data_editor(df, hide_index=True,height=350)
        elif choice == "High risk orders":
            if st.sidebar.button("Show orders"):
                hro_dict = func()   # returns { "RFM":df1 , "Scores":df2 , ... }

                for name, df in hro_dict.items():
                    st.subheader(name)     

                    fig = auto_plot(df)
                    st.plotly_chart(fig,width='stretch')    

                    st.data_editor(df, hide_index=True,height=350)

        elif func.__code__.co_argcount > 1:    # function has parameters
            param = st.sidebar.number_input("Enter parameter value:", value=5)
            if st.sidebar.button("Show"):

                df=func(param)
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)
        else:                                # no-parameter function
            if st.sidebar.button("Show"):

                df=func()
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)
else:
    st.sidebar.header("Prescriptive Analysis Functions")
    st.sidebar.write("What do you want to analyze?")
    
    analysis_functions = {
        "Unselected":None,
        "Products to discount":analytics.Products_to_Discount,
        "Products to Promote": analytics.Products_to_promote,
        "Customer Loyalty":analytics.Loyal_customers,
        "Customer Churning":analytics.Churning_customers,
        "Cities Needing Logistic Improving":analytics.Cities_improvement,
        "Ship Modes To Improve":analytics.Optimized_shipping
    }
    choice = st.sidebar.selectbox("Choose analysis", analysis_functions.keys())
    func = analysis_functions[choice]

    if func:
        if func.__code__.co_argcount > 1:    # function has parameters
            param = st.sidebar.number_input("Enter parameter value:", value=5)
            if st.sidebar.button("Show"):
                
                df=func(param)
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)
        else:                                # no-parameter function
            if st.sidebar.button("Show"):

                df=func()
                fig = auto_plot(df)
                st.plotly_chart(fig,width='stretch')

                st.data_editor(df,hide_index=True,height=350)
