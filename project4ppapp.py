import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings('ignore')


st.title("Interactive Retail Dashboard by Maxwell Adigwe")


url = "https://raw.githubusercontent.com/AbhisheakSaraswat/PythonStreamlit/main/Adidas.xlsx"
df_cleaned = pd.read_excel(url)


st.sidebar.header("Filters")
product = st.sidebar.multiselect("Select Product", options=df_cleaned["Product"].unique(), default=df_cleaned["Product"].unique())
state = st.sidebar.multiselect("Select State", options=df_cleaned["State"].unique(), default=df_cleaned["State"].unique())
city = st.sidebar.multiselect("Select City", options=df_cleaned["City"].unique(), default=df_cleaned["City"].unique())  # Added city filter
region = st.sidebar.multiselect("Select Region", options=df_cleaned["Region"].unique(), default=df_cleaned["Region"].unique())


df_cleaned = df_cleaned[(df_cleaned["Region"].isin(region)) & (df_cleaned["State"].isin(state)) & (df_cleaned["Product"].isin(product)) & (df_cleaned["City"].isin(city))]


df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['Day'] = df_cleaned['InvoiceDate'].dt.day
df_cleaned['Time'] = df_cleaned['InvoiceDate'].dt.time


city_list = [
    'New York', 'Houston', 'San Francisco', 'Los Angeles', 'Chicago', 'Dallas', 'Philadelphia', 'Las Vegas',
    'Denver', 'Seattle', 'Miami', 'Minneapolis', 'Billings', 'Knoxville', 'Omaha', 'Birmingham', 'Portland',
    'Anchorage', 'Honolulu', 'Orlando', 'Albany', 'Cheyenne', 'Richmond', 'Detroit', 'St. Louis', 'Salt Lake City',
    'New Orleans', 'Boise', 'Phoenix', 'Albuquerque', 'Atlanta', 'Charleston', 'Charlotte', 'Columbus', 'Louisville',
    'Jackson', 'Little Rock', 'Oklahoma City', 'Wichita', 'Sioux Falls', 'Fargo', 'Des Moines', 'Milwaukee',
    'Indianapolis', 'Baltimore', 'Wilmington', 'Newark', 'Hartford', 'Providence', 'Boston', 'Burlington', 'Manchester'
]

# Filter data for the cities
df_cities = df_cleaned[df_cleaned["City"].isin(city_list)]

# Map City to Codes (for demonstration purposes, you can use any valid code system)
city_to_code = {
    'New York': 'NYC', 'Houston': 'HOU', 'San Francisco': 'SF', 'Los Angeles': 'LA', 'Chicago': 'CHI', 
    'Dallas': 'DAL', 'Philadelphia': 'PHI', 'Las Vegas': 'LV', 'Denver': 'DEN', 'Seattle': 'SEA', 
    'Miami': 'MIA', 'Minneapolis': 'MIN', 'Billings': 'BIL', 'Knoxville': 'KNO', 'Omaha': 'OMA', 
    'Birmingham': 'BIR', 'Portland': 'POR', 'Anchorage': 'ANC', 'Honolulu': 'HON', 'Orlando': 'ORL', 
    'Albany': 'ALB', 'Cheyenne': 'CHY', 'Richmond': 'RIC', 'Detroit': 'DET', 'St. Louis': 'STL', 
    'Salt Lake City': 'SLC', 'New Orleans': 'NO', 'Boise': 'BOI', 'Phoenix': 'PHX', 'Albuquerque': 'ABQ', 
    'Atlanta': 'ATL', 'Charleston': 'CHA', 'Charlotte': 'CHA', 'Columbus': 'COL', 'Louisville': 'LUI', 
    'Jackson': 'JAC', 'Little Rock': 'LR', 'Oklahoma City': 'OKC', 'Wichita': 'WIC', 'Sioux Falls': 'SF', 
    'Fargo': 'FAR', 'Des Moines': 'DM', 'Milwaukee': 'MIL', 'Indianapolis': 'IND', 'Baltimore': 'BAL', 
    'Wilmington': 'WIL', 'Newark': 'NEW', 'Hartford': 'HAR', 'Providence': 'PRO', 'Boston': 'BOS', 
    'Burlington': 'BUR', 'Manchester': 'MAN'
}

# Add CityCode to the dataframe
df_cities['CityCode'] = df_cities['City'].map(city_to_code)

# Dashboard Layout with columns and rows
# First Row: Key Metrics Overview
col1, col2, col3 = st.columns([2, 4, 2])

with col1:
    # Total Sales
    total_sales = df_cleaned["TotalSales"].sum()
    st.metric("Total Sales ($)", f"${total_sales:,.2f}")

with col2:
    # Sales Trends
    st.subheader("Sales Trends")
    sales_trends = df_cleaned.groupby("InvoiceDate")["TotalSales"].sum().reset_index()
    st.line_chart(sales_trends.set_index("InvoiceDate"), use_container_width=True)

with col3:
    # Operating Profit
    total_profit = df_cleaned["OperatingProfit"].sum()
    st.metric("Operating Profit ($)", f"${total_profit:,.2f}")

# Second Row: Sales and Profit Analytics
col4, col5, col6 = st.columns([2, 4, 2])

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
    # Sales by Method
    sales_method = df_cleaned.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.subheader("Sales by Method")
    st.bar_chart(sales_method.set_index("SalesMethod"))

# Third Row: Regional and Top Products
col7, col8 = st.columns([2, 4])

with col7:
    # Regional Sales Distribution
    regional_sales = df_cleaned.groupby("Region")["TotalSales"].sum().reset_index()
    st.subheader("Regional Sales Distribution")
    st.bar_chart(regional_sales.set_index("Region"))

with col8:
    # Top Selling Products
    top_products = df_cleaned.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.subheader("Top 5 Selling Products")
    st.bar_chart(top_products.set_index("Product"))

col9, col10 = st.columns([2, 4])

with col9:
    # Total Sales by State
    st.subheader("Total Sales by State")
    state_to_code = {
        "New York": "NY", "Texas": "TX", "California": "CA", "Illinois": "IL", "Pennsylvania": "PA",
        "Nevada": "NV", "Colorado": "CO", "Washington": "WA", "Florida": "FL", "Minnesota": "MN",
        "Montana": "MT", "Tennessee": "TN", "Nebraska": "NE", "Alabama": "AL", "Maine": "ME",
        "Alaska": "AK", "Hawaii": "HI", "Wyoming": "WY", "Virginia": "VA", "Michigan": "MI",
        "Missouri": "MO", "Utah": "UT", "Oregon": "OR", "Louisiana": "LA", "Idaho": "ID",
        "Arizona": "AZ", "New Mexico": "NM", "Georgia": "GA", "South Carolina": "SC",
        "North Carolina": "NC", "Ohio": "OH", "Kentucky": "KY"
    }
    df_cleaned['StateCode'] = df_cleaned['State'].map(state_to_code)
    fig_sales_state = px.choropleth(
        df_cleaned,
        locations='StateCode',
        locationmode='USA-states',
        color='TotalSales',
        hover_name='State',
        hover_data={'TotalSales': ':.2f', 'OperatingProfit': ':.2f'},
        color_continuous_scale="Blues",
        labels={'TotalSales': 'Total Sales ($)', 'StateCode': 'State Code'},
        scope="usa",
        title=f"Total Sales by State",
        template="plotly_dark"  # Dark background
    )
    st.plotly_chart(fig_sales_state)

with col10:

    st.subheader("Operating Profit by State")
    fig_profit_state = px.choropleth(
        df_cleaned,
        locations='StateCode',
        locationmode='USA-states',
        color='OperatingProfit',
        hover_name='State',
        hover_data={'OperatingProfit': ':.2f', 'TotalSales': ':.2f'},
        color_continuous_scale="Reds",
        labels={'OperatingProfit': 'Operating Profit ($)', 'StateCode': 'State Code'},
        scope="usa",
        title=f"Operating Profit by State",
        template="plotly_dark"  # Dark background
    )
    st.plotly_chart(fig_profit_state)

col11, col12 = st.columns([2, 4])

with col11:

    st.subheader("Total Sales by City")
    fig_sales_city = px.choropleth(
        df_cities,
        locations='CityCode',
        locationmode='USA-states',
        color='TotalSales',
        hover_name='City',
        hover_data={'TotalSales': ':.2f', 'OperatingProfit': ':.2f'},
        color_continuous_scale="Blues",
        labels={'TotalSales': 'Total Sales ($)', 'CityCode': 'City Code'},
        scope="usa",
        title=f"Total Sales by City",
        template="plotly_dark"  # Dark background
    )
    st.plotly_chart(fig_sales_city)

with col12:
    # Operating Profit by City
    st.subheader("Operating Profit by City")
    fig_profit_city = px.choropleth(
        df_cities,
        locations='CityCode',
        locationmode='USA-states',
        color='OperatingProfit',
        hover_name='City',
        hover_data={'OperatingProfit': ':.2f', 'TotalSales': ':.2f'},
        color_continuous_scale="Reds",
        labels={'OperatingProfit': 'Operating Profit ($)', 'CityCode': 'City Code'},
        scope="usa",
        title=f"Operating Profit by City",
        template="plotly_dark"  # Dark background
    )
    st.plotly_chart(fig_profit_city)

st.markdown("### Click to View Details for States")
selected_state = st.selectbox("Select a State to View Details", options=df_cleaned["State"].unique())
filtered_data_state = df_cleaned[df_cleaned["State"] == selected_state]

st.markdown(f"#### Details for {selected_state}")
st.dataframe(filtered_data_state[["State", "TotalSales", "OperatingProfit"]])

st.markdown("### Click to View Details for Cities")
selected_city = st.selectbox("Select a City to View Details", options=df_cities["City"].unique())
filtered_data_city = df_cities[df_cities["City"] == selected_city]

st.markdown(f"#### Details for {selected_city}")
st.dataframe(filtered_data_city[["City", "TotalSales", "OperatingProfit"]])

st.markdown("### Map Tips")
st.info("""
- Hover over states and cities to see detailed information.
- Zoom in and out to explore specific regions.
- Filters applied to the dashboard will dynamically update these maps.
""")
