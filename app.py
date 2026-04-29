import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("pipeline_data.csv")

# Convert time column
df['time'] = pd.to_datetime(df['time'])

# Anomaly detection
df['alert'] = df['pressure'] > 80

print(df.head())

plt.figure(figsize=(12,8))

# Line graph
plt.subplot(2,1,1)
plt.plot(df['time'], df['pressure'])
plt.title("Pressure Over Time")

# Create hour column
df['hour'] = df['time'].dt.hour

# Create pivot table
pivot = df.pivot_table(
    values='pressure',
    index=df['time'].dt.minute,
    columns=df['time'].dt.hour
)

# Heatmap
plt.subplot(2,1,2)
sns.heatmap(pivot, cmap='coolwarm')
plt.title("Pressure Heatmap")

plt.tight_layout()
plt.show()