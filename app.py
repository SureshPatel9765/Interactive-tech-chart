import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time

# — Setup Google Sheets client from Streamlit secrets —
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scopes
)
client = gspread.authorize(creds)
data_sheet = client.open("Monthly or weekly  Technical Analysis Scanner").worksheet("Data")

# — Streamlit UI —
st.title("Live Tech Chart")

tickers = ["INFY", "TCS", "RELIANCE", "HDFCBANK"]
selected = st.selectbox("Select a Stock", tickers)

if st.button("Update & Plot"):
    # 1) Build the GOOGLEFINANCE formula string
    formula = (
        f'=GOOGLEFINANCE("NSE:{selected}",'
        '"all",TODAY()-250,TODAY())'
    )
    # 2) Write it into Data!A1 as a formula
    data_sheet.update_acell("A1", formula)

    st.write(f"✅ Updated Data!A1 with formula for **{selected}**. Fetching data…")
    # 3) Wait for Sheets to recalc
    time.sleep(5)

    # 4) Fetch the sheet’s records and plot
    records = data_sheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
        if {"Date", "Close"}.issubset(df.columns):
            df["Date"] = pd.to_datetime(df["Date"])
            st.line_chart(df.set_index("Date")["Close"])
        else:
            st.error("Required columns (‘Date’ & ‘Close’) not found in the sheet.")
    else:
        st.error("No data returned. Please wait a moment and try again.")
