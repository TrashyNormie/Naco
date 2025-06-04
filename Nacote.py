import streamlit as st
import pandas as pd

# URL to the published CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTYf3UdqcxtN-C8kjNYD1wpw0SAFbTVoo7Qqb9zcnLJVmsIqEOylv-T2mCKMOLsZVMMvtGPxfKxBxvC/pub?gid=0&single=true&output=csv"

# Read the data
df = pd.read_csv(CSV_URL)

# Show the full DataFrame (optional)
st.write("Live Data from Google Sheets", df)

# Example: show latest value from a 'Temperature' column
if not df.empty and 'Temperature' in df.columns:
    latest_temp = df['Temperature'].iloc[-1]
    st.metric("Latest Temperature", f"{latest_temp}°C")

    # Plot all values
    st.line_chart(df['Temperature'])
else:
    st.warning("Column 'Temperature' not found.")
