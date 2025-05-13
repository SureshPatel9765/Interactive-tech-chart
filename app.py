import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time

st.set_page_config(layout="wide")
st.title("Live-like OHLC Chart")

# 1. Dropdown for ticker selection
stock_list = ['NSE:TCS', 'NSE:INFY', 'NSE:RELIANCE','NSE:FORCEMOT']  # Add your preferred tickers
selected_stock = st.selectbox("Choose a Stock", stock_list)

# 2. Trigger Apps Script URL to update ticker in Data sheet
if st.button("Update Chart"):
    script_url = "https://script.google.com/macros/s/AKfycbw57Bx__2re0AnMBkBL8u0_8mITISgxy138cqijEZP5NwyhorPefJk-ajruRPtCj3UkhQ/exec"
    response = requests.get(f"{script_url}?stock={selected_stock}")
    if response.status_code == 200:
        st.success(f"Updated to {selected_stock}")
        time.sleep(15)  # Wait to allow GoogleFinance to update data
    else:
        st.error("Failed to update ticker")

# 3. Load updated OHLC data from Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFH0Am4UhvY6KaiFZEw5QhAP17wUog-QwhFY70h5SCUEsA2ZX6ccfNZlvf3sNV-KF9dlbjdP_6xt51/pub?gid=1177240346&single=true&output=csv"
df = pd.read_csv(sheet_url)

if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    window = st.slider("Number of recent candles", min_value=10, max_value=len(df), value=50)
    sub_df = df.tail(window)

    fig = go.Figure(data=[go.Candlestick(
        x=sub_df['Date'],
        open=sub_df['Open'],
        high=sub_df['High'],
        low=sub_df['Low'],
        close=sub_df['Close']
    )])

    fig.update_layout(xaxis_rangeslider_visible=False, height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not available. Please wait a few seconds and click 'Update Chart' again.")
