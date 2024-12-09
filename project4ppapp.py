import pandas as pd
import plotly.express as px
import streamlit as st
import warnings

warnings.filterwarnings('ignore')

st.title("Interactive Retail Dashboard by Maxwell Adigwe")

url = "https://raw.githubusercontent.com/AbhisheakSaraswat/PythonStreamlit/main/Adidas.xlsx"
df_cleaned = pd.read_excel(url)

st.sidebar.header("Filters")

# Multiselect for Product, Region, State, and City
product = st.sidebar.multiselect("Select Product", options=df_cleaned["Product"].unique(), default=df_cleaned["Product"].unique())
region = st.sidebar.multiselect("Select Region", options=df_cleaned["Region"].unique(), default=df_cleaned["Region"].unique())
state = st.sidebar.multiselect("Select State", options=df_cleaned["State"].unique(), default=df_cleaned["State"].unique())
city = st.sidebar.multiselect("Select City", options=df_cleaned["City"].unique(), default=df_cleaned["City"].unique())

# Apply filters based on selected multiselect values
df_cleaned = df_cleaned[(df_cleaned["Region"].isin(region)) & (df_cleaned["State"].isin(state)) & 
                        (df_cleaned["Product"].isin(product)) & (df_cleaned["City"].isin(city))]

df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['Day'] = df_cleaned['InvoiceDate'].dt.day
df_cleaned['Time'] = df_cleaned['InvoiceDate'].dt.time

# First Row: Key Metrics Overview
col1, col2 = st.columns(2)

with col1:
    # Total Sales
    total_sales = df_cleaned["TotalSales"].sum()
    st.metric("Total Sales ($)", f"${total_sales:,.2f}")

with col2:
    # Operating Profit
    total_profit = df_cleaned["OperatingProfit"].sum()
    st.metric("Operating Profit ($)", f"${total_profit:,.2f}")

col3, col4, col5, col6, col7 = st.columns(5)

with col3:
    # Sales by Method
    sales_method = df_cleaned.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.subheader("Sales by Method")
    st.bar_chart(sales_method.set_index("SalesMethod"))

with col4:
    # Yearly Sales vs Profit Comparison
    yearly_comparison = df_cleaned.groupby("Year")[["TotalSales", "OperatingProfit"]].sum().reset_index()
    yearly_comparison.columns = ["Year", "Total Sales", "Operating Profit"]
    st.subheader("Yearly Sales vs. Profit Comparison")
    st.bar_chart(yearly_comparison.set_index("Year"))

with col5:
    # Profit Margin Trends
    df_cleaned["ProfitMargin"] = (df_cleaned["OperatingProfit"] / df_cleaned["TotalSales"]) * 100
    yearly_profit_margin = df_cleaned.groupby("Year")["ProfitMargin"].mean().reset_index()
    st.subheader("Yearly Profit Margin Trends")
    st.line_chart(yearly_profit_margin.set_index("Year"), use_container_width=True)

with col6:
    # Regional Sales Distribution
    regional_sales = df_cleaned.groupby("Region")["TotalSales"].sum().reset_index()
    st.subheader("Regional Sales Distribution")
    st.bar_chart(regional_sales.set_index("Region"))

with col7:
    # Top Selling Products
    top_products = df_cleaned.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.subheader("Top 5 Selling Products")
    st.bar_chart(top_products.set_index("Product"))

# Second Row: Visuals (5 columns)
col8, col9, col10, col11, col12 = st.columns(5)

with col8:
    # Sales vs Operating Profit Scatter Plot
    st.subheader("Sales vs Operating Profit")
    fig_sales_profit = px.scatter(df_cleaned, x="TotalSales", y="OperatingProfit", color="Product", 
                                  title="Sales vs Operating Profit", template="plotly_dark")
    st.plotly_chart(fig_sales_profit)

with col9:
    # Monthly Sales Trends
    st.subheader("Monthly Sales Trends")
    monthly_sales = df_cleaned.groupby("Month")["TotalSales"].sum().reset_index()
    st.line_chart(monthly_sales.set_index("Month"), use_container_width=True)

with col10:
    # Profit Margin Distribution
    st.subheader("Profit Margin Distribution")
    st.write("A histogram to visualize the distribution of profit margins.")
    st.bar_chart(df_cleaned["ProfitMargin"])

with col11:
    # Profit vs Sales by Region (Scatter Plot)
    st.subheader("Profit vs Sales by Region")
    fig_profit_sales_region = px.scatter(df_cleaned, x="TotalSales", y="OperatingProfit", color="Region", 
                                         title="Profit vs Sales by Region", template="plotly_dark")
    st.plotly_chart(fig_profit_sales_region)

with col12:
    # Daily Sales Trends
    st.subheader("Daily Sales Trends")
    daily_sales = df_cleaned.groupby("Day")["TotalSales"].sum().reset_index()
    st.line_chart(daily_sales.set_index("Day"), use_container_width=True)

