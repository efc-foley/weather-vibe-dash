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
    
    # Feature 1: Unit Toggle
    unit = st.radio("Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
    temp_unit = "celsius" if "Celsius" in unit else "fahrenheit"
    
    # Date Range Setup
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    date_range = st.date_input("Select Date Range", [start_date, end_date])
    
    st.info("Searching is global! Type any city name.")

# 3. Logic: Geocoding & Weather Fetching
def get_coords(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    res = requests.get(geo_url).json()
    if "results" in res:
        return res["results"][0]["latitude"], res["results"][0]["longitude"]
    return None, None

def get_weather_data(city, start, end, unit):
    lat, lon = get_coords(city)
    if lat is None: return pd.DataFrame() # Handle city not found
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily=temperature_2m_max&temperature_unit={unit}&timezone=auto"
    response = requests.get(url).json()
    return pd.DataFrame({
        "Date": response["daily"]["time"],
        "Max Temp": response["daily"]["temperature_2m_max"],
        "City": city
    })

# Main Application logic
st.markdown("# ☀️ SkyCast Analytics")

if len(date_range) == 2:
    df_a = get_weather_data(city_a, date_range[0], date_range[1], temp_unit)
    df_b = get_weather_data(city_b, date_range[0], date_range[1], temp_unit)
    
    if not df_a.empty and not df_b.empty:
        combined_df = pd.concat([df_a, df_b])
        tab1, tab2 = st.tabs(["📈 Visualization", "📋 Data"])

        with tab1:
            col1, col2 = st.columns(2)
            unit_sym = "°C" if temp_unit == "celsius" else "°F"
            col1.metric(f"Avg Max Temp ({city_a})", f"{df_a['Max Temp'].mean():.1f} {unit_sym}")
            col2.metric(f"Avg Max Temp ({city_b})", f"{df_b['Max Temp'].mean():.1f} {unit_sym}")
            
            fig = px.line(combined_df, x="Date", y="Max Temp", color="City", 
                          template="plotly_dark", title=f"Historical Max Temperature ({unit_sym})")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Raw Weather Data")
            # Feature 3: Download Button
            csv = combined_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Data as CSV", data=csv, file_name="weather_data.csv", mime="text/csv")
            st.dataframe(combined_df, use_container_width=True)
    else:
        st.error("Could not find one of the cities. Please check the spelling!")