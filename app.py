import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Delivery Performance Dashboard", layout="wide")
st.title("📦 Last Mile Delivery Performance Dashboard")
st.write("Analyze delivery efficiency based on weather, traffic, vehicle, area, and category.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/delivery_data.csv")
    return df

df = load_data()

# Data cleaning
df = df.dropna()
mean_time = df['Delivery_Time'].mean()
std_time = df['Delivery_Time'].std()
df['Is_Late'] = df['Delivery_Time'] > (mean_time + std_time)
df['Agent_Age_Group'] = pd.cut(df['Agent_Age'], bins=[0,25,40,100], labels=['<25','25–40','40+'])

# Sidebar filters
st.sidebar.header("🔍 Filters")
weather_filter = st.sidebar.multiselect("Weather", df['Weather'].unique())
traffic_filter = st.sidebar.multiselect("Traffic", df['Traffic'].unique())
vehicle_filter = st.sidebar.multiselect("Vehicle Type", df['Vehicle'].unique())
category_filter = st.sidebar.multiselect("Category", df['Category'].unique())
area_filter = st.sidebar.multiselect("Area", df['Area'].unique())

filtered_df = df.copy()
if weather_filter:
    filtered_df = filtered_df[filtered_df['Weather'].isin(weather_filter)]
if traffic_filter:
    filtered_df = filtered_df[filtered_df['Traffic'].isin(traffic_filter)]
if vehicle_filter:
    filtered_df = filtered_df[filtered_df['Vehicle'].isin(vehicle_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
if area_filter:
    filtered_df = filtered_df[filtered_df['Area'].isin(area_filter)]

# Key metrics
st.sidebar.header("📊 Key Metrics")
avg_time = round(filtered_df['Delivery_Time'].mean(), 2)
late_pct = round(filtered_df['Is_Late'].mean() * 100, 2)
st.sidebar.metric("Average Delivery Time", f"{avg_time} mins")
st.sidebar.metric("Late Deliveries (%)", f"{late_pct}%")

# 1️⃣ Delay Analyzer
st.subheader("⏱️ Delay Analyzer (Weather vs Traffic)")
delay_chart = filtered_df.groupby(['Weather', 'Traffic'])['Delivery_Time'].mean().reset_index()
fig1 = px.bar(delay_chart, x='Weather', y='Delivery_Time', color='Traffic', barmode='group',
              title="Average Delivery Time by Weather & Traffic")
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Vehicle Comparison
st.subheader("🚚 Vehicle Performance Comparison")
vehicle_chart = filtered_df.groupby('Vehicle')['Delivery_Time'].mean().reset_index()
fig2 = px.bar(vehicle_chart, x='Vehicle', y='Delivery_Time', color='Vehicle',
              title="Average Delivery Time by Vehicle Type")
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Agent Performance
st.subheader("👷 Agent Performance")
fig3 = px.scatter(filtered_df, x='Agent_Rating', y='Delivery_Time', color='Agent_Age_Group',
                  title="Agent Rating vs Delivery Time", hover_data=['Agent_Age'])
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Area Heatmap
st.subheader("📍 Area Heatmap")
area_chart = filtered_df.groupby('Area')['Delivery_Time'].mean().reset_index()
fig4 = px.density_heatmap(area_chart, x='Area', y='Delivery_Time', color_continuous_scale='YlOrRd',
                          title="Average Delivery Time by Area")
st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Category Visualizer
st.subheader("📦 Category Visualizer")
fig5 = px.box(filtered_df, x='Category', y='Delivery_Time', color='Category',
              title="Delivery Time Distribution by Category")
st.plotly_chart(fig5, use_container_width=True)

st.success("✅ Dashboard ready! Adjust filters to explore insights.")
