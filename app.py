import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set Page Configuration (Fixes the theme and layout)
st.set_page_config(page_title="SkyCast Analytics", layout="wide")

# 2. Sidebar Setup (Dashboard Controls)
with st.sidebar:
    st.header("Dashboard Controls")
    city_a = st.selectbox("City A", ["New York", "London", "Tokyo", "Paris"], index=0)
    city_b = st.selectbox("City B", ["London", "New York", "Tokyo", "Paris"], index=1)
    date_range = st.date_input("Select Date Range")
    update_btn = st.button("Update Dashboard", type="primary")

# 3. Main Header (Fixes the missing title)
st.markdown("# ☀️ SkyCast Analytics")

# 4. Tabs and Metrics
tab1, tab2 = st.tabs(["📈 Visualization", "📋 Data"])

with tab1:
    # Metric cards (Matching your demo values)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Avg Max Temp ({city_a})", value="0.8 °C")
    with col2:
        st.metric(label=f"Avg Max Temp ({city_b})", value="8.2 °C")
    
    # Placeholder for your Plotly chart
    st.info("Charts will load here once the data processing code is added below.")

# 5. Data Processing Logic (Add your notebook's data functions here)
with tab1:
    # Metric cards (Existing)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Avg Max Temp ({city_a})", value="0.8 °C")
    with col2:
        st.metric(label=f"Avg Max Temp ({city_b})", value="8.2 °C")
    
    # --- ADD THIS: Graph Logic ---
    st.subheader(f"Temperature Comparison: {city_a} vs {city_b}")
    
    # Create sample data (In a real app, this would come from your Open-Meteo API call)
    chart_data = pd.DataFrame({
        'Date': pd.date_range(start='2026-01-06', periods=30),
        city_a: [5, 6, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3],
        city_b: [8, 9, 8, 7, 6, 7, 8, 9, 10, 11, 12, 11, 10, 9, 8, 7, 6, 7, 8, 9, 10, 11, 12, 13, 14, 13, 12, 11, 10, 9]
    })
    
    # Melt the data for Plotly (This makes it easier to color by City)
    df_melted = chart_data.melt(id_vars=['Date'], var_name='City', value_name='Temperature (°C)')
    
    # Create the Line Chart
    fig = px.line(df_melted, x='Date', y='Temperature (°C)', color='City',
                  template="plotly_dark", # Matches your dark theme
                  color_discrete_sequence=['#00d4ff', '#ff4b4b']) # New York Blue and London Red
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)