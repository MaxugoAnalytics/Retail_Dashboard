import pandas as pd
import plotly.express as px
import streamlit as st
import warnings

warnings.filterwarnings('ignore')

# Set the page configuration for full-width layout
st.set_page_config(page_title="Retail Dashboard", layout="wide")

st.title("Interactive Retail Dashboard by Maxwell Adigwe")

# Load data
url = "https://raw.githubusercontent.com/AbhisheakSaraswat/PythonStreamlit/main/Adidas.xlsx"
df_cleaned = pd.read_excel(url)

# Preprocess data
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['Day'] = df_cleaned['InvoiceDate'].dt.day
df_cleaned['Hour'] = df_cleaned['InvoiceDate'].dt.hour
df_cleaned['ProfitMargin'] = (df_cleaned["OperatingProfit"] / df_cleaned["TotalSales"]) * 100

# Function to handle "Select All" logic
def apply_filter(options, selected):
    if "All" in selected:
        return options
    return selected

# First Row: Four Visualizations
st.markdown("### Key Metrics and Trends")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Sales by Method")
    with st.expander("Filter by Sales Method"):
        method_options = ["All"] + df_cleaned["SalesMethod"].unique().tolist()
        method_filter = st.multiselect("Select Methods", method_options, default="All")
    filtered_method = df_cleaned[df_cleaned["SalesMethod"].isin(apply_filter(method_options, method_filter))]
    sales_method = filtered_method.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_method.set_index("SalesMethod"), use_container_width=True)

with col2:
    st.subheader("Yearly Sales vs Profit")
    with st.expander("Filter by Year"):
        year_options = ["All"] + df_cleaned["Year"].unique().tolist()
        year_filter = st.multiselect("Select Years", year_options, default="All")
    filtered_year = df_cleaned[df_cleaned["Year"].isin(apply_filter(year_options, year_filter))]
    yearly_comparison = filtered_year.groupby("Year")[["TotalSales", "OperatingProfit"]].sum().reset_index()
    st.bar_chart(yearly_comparison.set_index("Year"), use_container_width=True)

with col3:
    st.subheader("Yearly Profit Margin Trends")
    with st.expander("Filter by Product"):
        product_options = ["All"] + df_cleaned["Product"].unique().tolist()
        product_filter = st.multiselect("Select Products", product_options, default="All")
    filtered_product = df_cleaned[df_cleaned["Product"].isin(apply_filter(product_options, product_filter))]
    yearly_profit_margin = filtered_product.groupby("Year")["ProfitMargin"].mean().reset_index()
    st.line_chart(yearly_profit_margin.set_index("Year"), use_container_width=True)

with col4:
    st.subheader("Daily Sales Trends")
    daily_sales = df_cleaned.groupby("Day")["TotalSales"].sum().reset_index()
    st.line_chart(daily_sales.set_index("Day"), use_container_width=True)

# Second Row: Four More Visualizations
st.markdown("### Additional Insights")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.subheader("Regional Sales Distribution")
    with st.expander("Filter by Region"):
        region_options = ["All"] + df_cleaned["Region"].unique().tolist()
        region_filter = st.multiselect("Select Regions", region_options, default="All")
    filtered_region = df_cleaned[df_cleaned["Region"].isin(apply_filter(region_options, region_filter))]
    regional_sales = filtered_region.groupby("Region")["TotalSales"].sum().reset_index()
    st.bar_chart(regional_sales.set_index("Region"), use_container_width=True)

with col6:
    st.subheader("Top Selling Products")
    with st.expander("Filter by State"):
        state_options = ["All"] + df_cleaned["State"].unique().tolist()
        state_filter = st.multiselect("Select States", state_options, default="All")
    filtered_state = df_cleaned[df_cleaned["State"].isin(apply_filter(state_options, state_filter))]
    top_products = filtered_state.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.bar_chart(top_products.set_index("Product"), use_container_width=True)

with col7:
    st.subheader("Top Selling States")
    top_states = df_cleaned.groupby("State")["TotalSales"].sum().nlargest(5).reset_index()
    st.bar_chart(top_states.set_index("State"), use_container_width=True)

with col8:
    st.subheader("Profit vs Sales by Region")
    fig_profit_sales_region = px.scatter(
        df_cleaned, 
        x="TotalSales", 
        y="OperatingProfit", 
        color="Region", 
        template="plotly_dark"
    )
    st.plotly_chart(fig_profit_sales_region, use_container_width=True)

