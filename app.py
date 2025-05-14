import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import requests

st.set_page_config(layout="wide")
st.title("Live-like OHLC Chart")

# Dropdown to select ticker
tickers = ["NSE:RELIANCE", "NSE:TCS", "NSE:HDFCBANK", "NSE:INFY"]
ticker = st.selectbox("Select Ticker", tickers)

# Step 1: Update Google Sheet via Apps Script
update_url = f"https://script.google.com/macros/s/AKfycbw57Bx__2re0AnMBkBL8u0_8mITISgxy138cqijEZP5NwyhorPefJk-ajruRPtCj3UkhQ/exec?stock={ticker}"
st.text(f"Updating Google Sheet for {ticker}...")
requests.get(update_url)

# Step 2: Wait for Google Sheets to refresh
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFH0Am4UhvY6KaiFZEw5QhAP17wUog-QwhFY70h5SCUEsA2ZX6ccfNZlvf3sNV-KF9dlbjdP_6xt51/pub?gid=1177240346&single=true&output=csv"

max_retries = 10
for i in range(max_retries):
    try:
        df = pd.read_csv(csv_url)
        if "Date" in df.columns and len(df) > 3:
            break
    except:
        pass
    st.text("Waiting for data update...")
    time.sleep(1)
else:
    st.error("Data not updated. Try again.")
    st.stop()

# Step 3: Prepare and show chart
df = df.sort_values('Date')
df['Date'] = pd.to_datetime(df['Date'])

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
