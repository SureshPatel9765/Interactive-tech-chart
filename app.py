import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time
import requests

# === Setup Google Sheets access ===
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets.gcp_service_account, scopes=scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Monthly or weekly  Technical Analysis Scanner")
data_sheet = sheet.worksheet("Data")

# === Ticker dropdown ===
tickers = ["INFY", "TCS", "RELIANCE", "HDFCBANK"]
selected = st.selectbox("Select a Stock", tickers)

if st.button("Update Ticker"):
    data_sheet.update("A1", selected)
    time.sleep(5)
    data = data_sheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    if "Date" in df.columns and "Close" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        st.line_chart(df.set_index("Date")["Close"])
    else:
        st.write("Required columns not found in the sheet.")
