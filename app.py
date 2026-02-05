import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="SkyCast Analytics", layout="wide")

# 2. Sidebar Setup
with st.sidebar:
    st.header("Dashboard Controls")
    city_a = st.text_input("City A", "New York")
    city_b = st.text_input("City B", "London")
    
    # Default to last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    date_range = st.date_input("Select Date Range", [start_date, end_date])
    
    update_btn = st.button("Update Dashboard", type="primary")

# 3. Main Header
st.markdown("# ☀️ SkyCast Analytics")

# 4. Data Fetching Logic (Open-Meteo API)
def get_weather_data(city, start, end):
    # For a production app, you'd use a geocoding API. 
    # For this demo, we use hardcoded coordinates for common cities.
    coords = {"New York": (40.71, -74.00), "London": (51.50, -0.12), "Tokyo": (35.68, 139.69)}
    lat, lon = coords.get(city, (40.71, -74.00)) # Default to NY if not found
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily=temperature_2m_max&timezone=auto"
    response = requests.get(url).json()
    return pd.DataFrame({
        "Date": response["daily"]["time"],
        "Max Temp": response["daily"]["temperature_2m_max"],
        "City": city
    })

# Fetch Data
if len(date_range) == 2:
    df_a = get_weather_data(city_a, date_range[0], date_range[1])
    df_b = get_weather_data(city_b, date_range[0], date_range[1])
    combined_df = pd.concat([df_a, df_b])

    # 5. Tabs
    tab1, tab2 = st.tabs(["📈 Visualization", "📋 Data"])

    with tab1:
        # Metric Cards (Only once)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Avg Max Temp ({city_a})", value=f"{df_a['Max Temp'].mean():.1f} °C")
        with col2:
            st.metric(label=f"Avg Max Temp ({city_b})", value=f"{df_b['Max Temp'].mean():.1f} °C")
        
        # Line Chart comparing both
        fig = px.line(combined_df, x="Date", y="Max Temp", color="City",
                      title=f"Max Daily Temperature: {city_a} vs {city_b}",
                      labels={"Max Temp": "Temperature (°C)"})
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Raw Weather Data")
        st.dataframe(combined_df, use_container_width=True)