import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import warnings
warnings.filterwarnings('ignore')
import os

Create a file uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    df_cleaned = pd.read_excel(uploaded_file)

    # Sidebar for filters
    st.title("Nalytics Retail Dashboard by Maxwell Adigwe")
    st.sidebar.header("Filters")
    product = st.sidebar.multiselect("Select Product", options=df_cleaned["Product"].unique(), default=df_cleaned["Product"].unique())
    state = st.sidebar.multiselect("Select State", options=df_cleaned["State"].unique(), default=df_cleaned["State"].unique())
    region = st.sidebar.multiselect("Select Region", options=df_cleaned["Region"].unique(), default=df_cleaned["Region"].unique())

    # Refine the dataframe based on filters
    df_cleaned = df_cleaned[(df_cleaned["Region"].isin(region)) & (df_cleaned["State"].isin(state)) & (df_cleaned["Product"].isin(product))]

    # Plotting setup
    st.subheader("Refined Data")
    st.dataframe(df_cleaned)

    # Add datetime components
    df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
    df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
    df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
    df_cleaned['Day'] = df_cleaned['InvoiceDate'].dt.day
    df_cleaned['Time'] = df_cleaned['InvoiceDate'].dt.time

    # Sales and Profit Trends
    sales_trends = df_cleaned.groupby("InvoiceDate")["TotalSales"].sum().reset_index()
    profit_trends = df_cleaned.groupby("InvoiceDate")["OperatingProfit"].sum().reset_index()

    # Rename columns for clarity
    sales_trends.columns = ["InvoiceDate", "Total Sales"]
    profit_trends.columns = ["InvoiceDate", "Operating Profit"]

    # Plot the sales and profit trends
    st.subheader("Sales and Profit Analytical Trends")
    st.subheader("Sales Trends")
    st.line_chart(sales_trends.set_index("InvoiceDate"), use_container_width=True)
    st.subheader("Profit Trends")
    st.line_chart(profit_trends.set_index("InvoiceDate"), use_container_width=True)

    # Yearly Sales vs Profit Comparison
    yearly_comparison = pd.DataFrame({"Year": sales_trends.index, "Total Sales": sales_trends["Total Sales"], "Operating Profit": profit_trends["Operating Profit"]})
    st.subheader("Yearly Sales vs. Profit Comparison")
    # Fixing the color error: Providing colors for each column
    colors = ['#00FF00', '#FF0000']  # Green for 'Total Sales', Red for 'Operating Profit'
    st.bar_chart(yearly_comparison.set_index("Year"), color=colors)

    # Sales by Method
    sales_method = df_cleaned.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.subheader("Sales by Method")
    st.bar_chart(sales_method.set_index("SalesMethod"), color='#00FF00')

    # Use a single color code
    # Top Selling Products
    top_products = df_cleaned.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.subheader("Top 5 Selling Products")
    st.bar_chart(top_products.set_index("Product"), color='#00FF00')

    # Regional Sales Distribution
    regional_sales = df_cleaned.groupby("Region")["TotalSales"].sum().reset_index()
    st.subheader("Regional Sales Distribution")
    st.bar_chart(regional_sales.set_index("Region"), color='#00FF00')

    # Monthly Sales Trends
    monthly_sales = df_cleaned.groupby("Month")["TotalSales"].sum().reset_index()
    st.subheader("Monthly Sales Trends")
    st.line_chart(monthly_sales.set_index("Month"), use_container_width=True)

    # Profit Margin Trends
    df_cleaned["ProfitMargin"] = (df_cleaned["OperatingProfit"] / df_cleaned["TotalSales"]) * 100
    yearly_profit_margin = df_cleaned.groupby("Year")["ProfitMargin"].mean().reset_index()
    st.subheader("Yearly Profit Margin Trends")
    st.line_chart(yearly_profit_margin.set_index("Year"), use_container_width=True)
