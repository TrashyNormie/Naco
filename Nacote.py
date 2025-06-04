
import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(layout="wide")
st.title("📊 Monitoreo en Tiempo Real desde Google Sheets")

# Replace this with your actual published-to-web CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTYf3UdqcxtN-C8kjNYD1wpw0SAFbTVoo7Qqb9zcnLJVmsIqEOylv-T2mCKMOLsZVMMvtGPxfKxBxvC/pub?gid=0&single=true&output=csv"

# Auto-refresh every 60 seconds
count = st.experimental_autorefresh(interval=1000, key="datarefresh")

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = [col.strip() for col in df.columns]
    return df

df_raw = load_data(CSV_URL)

# --- CLEAN DATA ---
def clean_column(col):
    return pd.to_numeric(
        df_raw[col].astype(str).str.replace(",", ".", regex=False),
        errors='coerce'
    )

df_raw['FECHA Y HORA'] = pd.to_datetime(df_raw['FECHA Y HORA'], errors='coerce', dayfirst=True)

cols = ['CORRIENTE', 'VOLTAJE', 'POTENCIA', 'ENERGIA', 'FRECUENCIA']
df = df_raw.copy()
for col in cols:
    df[col] = clean_column(col)

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

# --- PLOTS ---
st.subheader("📉 Gráficas de Evolución Temporal")
for col in cols:
    st.line_chart(df.set_index('FECHA Y HORA')[col], height=200, use_container_width=True)

