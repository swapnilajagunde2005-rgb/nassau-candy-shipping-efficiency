
import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Nassau Candy Logistics Dashboard", layout="wide")

st.title("🏭 Factory-to-Customer Shipping Route Efficiency Dashboard")
st.markdown("Automated Operational Intelligence for Nassau Candy Distributor")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('nassau_cleaned_delivery_data.csv')
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Controls")

# Region Filter
regions = ['All'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Ship Mode Filter
modes = ['All'] + list(df['Ship Mode'].unique())
selected_mode = st.sidebar.selectbox("Select Shipping Mode", modes)

# Lead Time Threshold Slider
max_days = int(df['Shipping Lead Time'].max())
min_days = int(df['Shipping Lead Time'].min())
threshold = st.sidebar.slider("Highlight Routes Exceeding (Days)", min_days, max_days, 1400)

# Apply filters
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_mode != 'All':
    filtered_df = filtered_df[filtered_df['Ship Mode'] == selected_mode]

# --- MAIN DASHBOARD MODULES ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Orders Fulfilled", f"{len(filtered_df):,}")
with col2:
    st.metric("Average Lead Time", f"{filtered_df['Shipping Lead Time'].mean():.2f} Days")
with col3:
    st.metric("Active Distribution Routes", f"{filtered_df['Route'].nunique()}")

# --- LEADERBOARDS ---
st.subheader("📊 Route Performance Leaderboards")
col_left, col_right = st.columns(2)

route_summary = filtered_df.groupby('Route').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Total_Orders=('Order ID', 'count')
).reset_index()

# Keep stable routes
stable_routes = route_summary[route_summary['Total_Orders'] >= 5]

with col_left:
    st.write("🏆 **Top 5 Most Efficient Routes (Fastest)**")
    st.dataframe(stable_routes.sort_values(by='Avg_Lead_Time').head(5), use_container_width=True)

with col_right:
    st.write("⚠️ **Bottom 5 Logistical Bottlenecks (Slowest)**")
    st.dataframe(stable_routes.sort_values(by='Avg_Lead_Time', ascending=False).head(5), use_container_width=True)

# --- SHIP MODE TRANSIT COMPARISON ---
st.subheader("🚛 Shipping Mode Tradeoff Analysis")
mode_analysis = filtered_df.groupby('Ship Mode').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Total_Shipments=('Order ID', 'count')
).reset_index()
st.bar_chart(data=mode_analysis, x='Ship Mode', y='Avg_Lead_Time', use_container_width=True)

st.success("Dashboard components compiled and ready for live server deployment!")
