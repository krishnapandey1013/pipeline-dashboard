import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Pipeline Dashboard", layout="wide")

# Title
st.title("🚀 Smart Pipeline Monitoring Dashboard")
st.caption("Real-time monitoring of pipeline pressure with anomaly detection and interactive visualization.")

# Load data
df = pd.read_csv("pipeline_data.csv")
df['time'] = pd.to_datetime(df['time'])

df['pressure_smooth'] = df['pressure'].rolling(5).mean().fillna(method='bfill')

# Anomaly detection
mean = df['pressure'].mean()
std = df['pressure'].std()

df['alert'] = df['pressure'] > (mean + 1.5 * std)

# Sidebar filter
st.sidebar.header("Filter Data")
selected_hours = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))

df['hour'] = df['time'].dt.hour
filtered_df = df[(df['hour'] >= selected_hours[0]) & (df['hour'] <= selected_hours[1])]

# Show metrics
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Pressure", round(filtered_df['pressure'].mean(), 2))
col2.metric("Max Pressure", round(filtered_df['pressure'].max(), 2))
col3.metric("Alerts", filtered_df['alert'].sum())
col4.metric("Min Pressure", round(filtered_df['pressure'].min(), 2))

# Line chart
st.subheader("📈 Pressure Over Time")

filtered_df['pressure_smooth'] = (
    filtered_df['pressure']
    .rolling(5)
    .mean()
    .fillna(method='bfill')
)

st.line_chart(
    filtered_df.set_index('time')[['pressure', 'pressure_smooth']]
)

# Smooth pressure line
filtered_df['pressure_smooth'] = filtered_df['pressure'].rolling(5).mean().fillna(method='bfill')

# Heatmap
st.subheader("🔥 Pressure Heatmap")

pivot = filtered_df.pivot_table(
    values='pressure',
    index=filtered_df['time'].dt.minute,
    columns=filtered_df['time'].dt.hour
)

fig, ax = plt.subplots()
sns.heatmap(pivot, cmap='coolwarm', ax=ax)

ax.set_xlabel("Hour")
ax.set_ylabel("Minute")

st.pyplot(fig)

st.markdown("---")

# Show alerts
st.subheader("🚨 Alerts Data")

alerts_df = filtered_df[filtered_df['alert'] == True]
alerts_df = alerts_df.sort_values(by='pressure', ascending=False)

if not alerts_df.empty:
    st.error("⚠️ High Pressure Detected!")
    st.dataframe(alerts_df, use_container_width=True)
else:
    st.success("✅ No Critical Alerts")