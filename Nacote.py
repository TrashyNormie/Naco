import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(layout="wide")
st.title("📊 Monitoreo en Tiempo Real desde Google Sheets")

# CSV export link from your Google Sheet
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTYf3UdqcxtN-C8kjNYD1wpw0SAFbTVoo7Qqb9zcnLJVmsIqEOylv-T2mCKMOLsZVMMvtGPxfKxBxvC/pub?gid=0&single=true&output=csv"

# --- AUTO REFRESH ---
# Refreshes every 1 second (1000 ms)
st.experimental_autorefresh(interval=1000, key="datarefresh")

# --- LOAD DATA ---
@st.cache_data(ttl=1)  # cache expires every second
def load_data(url):
    df = pd.read_csv(url)
    df.columns = [col.strip() for col in df.columns]
    return df

df_raw = load_data(CSV_URL)

# --- CLEAN DATA ---
def clean_column(col):
    return pd.to_numeric(
        df_raw[col]
        .astype(str)
        .str.replace(",", "", regex=False)   # Remove thousands separator
        .str.strip(),                        # Remove leading/trailing whitespace
        errors='coerce'
    )

# Parse datetime column
df_raw['FECHA Y HORA'] = pd.to_datetime(df_raw['FECHA Y HORA'], errors='coerce', dayfirst=True)

# Clean numeric columns
cols = ['CORRIENTE', 'VOLTAJE', 'POTENCIA', 'ENERGIA', 'FRECUENCIA']
df = df_raw.copy()
for col in cols:
    df[col] = clean_column(col)

# Drop invalid rows
df.dropna(subset=['FECHA Y HORA'], inplace=True)
df.dropna(subset=cols, how='all', inplace=True)

# --- DISPLAY METRICS ---
st.subheader("📈 Últimos Valores")
col1, col2, col3, col4, col5 = st.columns(5)
latest_row = df.iloc[-1]

col1.metric("⚡ Corriente", f"{latest_row['CORRIENTE']:.2f}")
col2.metric("🔌 Voltaje", f"{latest_row['VOLTAJE']:.2f}")
col3.metric("🔥 Potencia", f"{latest_row['POTENCIA']:.2f}")
col4.metric("⚙️ Energía", f"{latest_row['ENERGIA']:.2f}")
col5.metric("🎵 Frecuencia", f"{latest_row['FRECUENCIA']:.2f}")

# Show last update timestamp
st.caption(f"🕒 Última actualización de datos: {latest_row['FECHA Y HORA'].strftime('%Y-%m-%d %H:%M:%S')}")

# --- PLOTS ---
st.subheader("📉 Gráficas de Evolución Temporal")
for col in cols:
    st.line_chart(df.set_index('FECHA Y HORA')[col], height=200, use_container_width=True)
