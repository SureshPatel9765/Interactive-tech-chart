import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time

# 1) Setup Google Sheets client
scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
data_sheet = client.open("Monthly or weekly  Technical Analysis Scanner").worksheet("Data")

# 2) Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None

# 3) UI
st.title("Live Tech Chart (Approach 2)")
tickers = ["INFY","TCS","RELIANCE","HDFCBANK"]
selected = st.selectbox("Select a Stock", tickers)

if st.button("Update & Plot"):
    data_sheet.update("A1", selected)
    st.write(f"✅ Updated ticker to **{selected}**, fetching new data…")
    time.sleep(5)

    data = data_sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        if {"Date","Close"}.issubset(df.columns):
            df["Date"] = pd.to_datetime(df["Date"])
            st.session_state.df = df
        else:
            st.error("Required columns missing.")
    else:
        st.error("No data returned.")

# 4) Always render chart if available
if st.session_state.df is not None:
    st.line_chart(st.session_state.df.set_index("Date")["Close"])
