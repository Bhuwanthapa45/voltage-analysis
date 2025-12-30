import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Title of the Web App
st.title("Voltage Data Analysis Dashboard")
st.write("This dashboard visualizes the voltage trends and identifies anomalies.")

# 1. Load Data
# We use st.cache_data to make it faster
@st.cache_data
def load_data():
    df = pd.read_csv('Sample_Data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S')
    df = df.rename(columns={'Values': 'Voltage'})
    df = df.sort_values('Timestamp')
    df.set_index('Timestamp', inplace=True)
    return df

try:
    df = load_data()
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Error: Sample_Data.csv not found. Please upload it to the repository.")
    st.stop()

# 2. Moving Average
df['MA_5Day'] = df['Voltage'].rolling(window='5D').mean()

# 3. Plotting
st.subheader("Voltage vs Timestamp Chart")
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(df.index, df['Voltage'], label='Voltage', color='#1f77b4', alpha=0.6)
ax.plot(df.index, df['MA_5Day'], label='5-Day Moving Average', color='red', linewidth=2)
ax.set_title('Voltage vs Timestamp')
ax.set_xlabel('Timestamp')
ax.set_ylabel('Voltage')
ax.legend()
ax.grid(True)

# Display the plot in the app
st.pyplot(fig)

# 4. Analysis
st.subheader("Key Statistics")
peaks_indices, _ = find_peaks(df['Voltage'], distance=20)
st.write(f"**Number of Local Peaks:** {len(peaks_indices)}")

# Bonus Analysis
below_20 = df[df['Voltage'] < 20]
st.write(f"**Instances below 20V:** {len(below_20)}")

# Show Raw Data (Optional)
if st.checkbox('Show Raw Data'):
    st.write(df)