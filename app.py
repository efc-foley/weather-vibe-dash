import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="SkyCast Analytics",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Light Mode / Premium look
st.markdown("""
<style>
    /* Force a light background for the app content area */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Premium Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: white !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid #e5e7eb !important;
        text-align: center;
    }

    /* Force text colors for visibility inside metric cards */
    [data-testid="stMetricLabel"] {
        color: #4b5563 !important;
    }
    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

def get_coordinates(city_name):
    """Fetch latitude and longitude for a city name using Open-Meteo Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get('results'):
        result = response.json()['results'][0]
        return result['latitude'], result['longitude'], result['name'], result.get('country', '')
    return None, None, None, None

def get_weather_data(lat, lon, start_date, end_date):
    """Fetch historical max daily temperature."""
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['daily']
        df = pd.DataFrame({
            'Date': pd.to_datetime(data['time']),
            'Max Temp (°C)': data['temperature_2m_max']
        })
        return df
    return pd.DataFrame()

# Header
st.title("🌤️ SkyCast Analytics")
st.markdown("Compare historical temperature trends between two cities.")

# Sidebar Controls
st.sidebar.header("Dashboard Controls")
city_a_name = st.sidebar.text_input("City A", value="New York")
city_b_name = st.sidebar.text_input("City B", value="London")

default_start = datetime.now() - timedelta(days=30)
default_end = datetime.now() - timedelta(days=1)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(default_start, default_end),
    max_value=datetime.now() - timedelta(days=1)
)

if len(date_range) == 2:
    start_date, end_date = date_range
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    if st.sidebar.button("Update Dashboard", type="primary"):
        with st.spinner("Fetching data..."):
            # Fetch Coords
            lat_a, lon_a, name_a, country_a = get_coordinates(city_a_name)
            lat_b, lon_b, name_b, country_b = get_coordinates(city_b_name)

            if lat_a and lat_b:
                # Fetch Weather
                df_a = get_weather_data(lat_a, lon_a, start_str, end_str)
                df_b = get_weather_data(lat_b, lon_b, start_str, end_str)

                if not df_a.empty and not df_b.empty:
                    # Combine Data
                    df_a['City'] = f"{name_a}, {country_a}"
                    df_b['City'] = f"{name_b}, {country_b}"
                    combined_df = pd.concat([df_a, df_b])

                    # Tabs
                    tab1, tab2 = st.tabs(["📈 Visualization", "📋 Data Table"])

                    with tab1:
                        st.subheader(f"Max Daily Temperature: {name_a} vs {name_b}")
                        
                        # Quick Stats Summary moved above the chart
                        col1, col2 = st.columns(2)
                        with col1:
                            avg_a = df_a['Max Temp (°C)'].mean()
                            st.metric(f"Avg Max Temp ({name_a})", f"{avg_a:.1f} °C")
                        with col2:
                            avg_b = df_b['Max Temp (°C)'].mean()
                            st.metric(f"Avg Max Temp ({name_b})", f"{avg_b:.1f} °C")

                        fig = px.line(
                            combined_df, 
                            x='Date', 
                            y='Max Temp (°C)', 
                            color='City',
                            template='plotly_white',
                            color_discrete_sequence=px.colors.qualitative.Safe
                        )
                        fig.update_layout(
                            hovermode="x unified",
                            xaxis_title="Date",
                            yaxis_title="Max Temperature (°C)",
                            legend_title="City",
                            font=dict(family="Arial, sans-serif", size=12)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with tab2:
                        st.subheader("Raw Historical Data")
                        pivot_df = combined_df.pivot(index='Date', columns='City', values='Max Temp (°C)')
                        st.dataframe(pivot_df, use_container_width=True)
                else:
                    st.error("Could not fetch weather data for the selected range.")
            else:
                st.error("Could not find coordinates for one or both cities. Please check the spelling.")
else:
    st.info("Please select a valid start and end date.")

# Footer
st.markdown("---")
st.markdown("Data provided by [Open-Meteo](https://open-meteo.com/).")
