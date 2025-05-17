import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import requests

# === Setup Google Sheets access ===
"scope = [""https://spreadsheets.google.com/feeds"", ""https://www.googleapis.com/auth/drive""]"
"creds = ServiceAccountCredentials.from_json_keyfile_name(""credentials.json"", scope)"
client = gspread.authorize(creds)

# Open your sheet
"sheet = client.open(""Monthly or weekly  Technical Analysis Scanner"")"
"#control_sheet = sheet.worksheet(""Control"")"
"data_sheet = sheet.worksheet(""Data"")"

# === Ticker dropdown ===
"tickers = [""INFY"", ""TCS"", ""RELIANCE"", ""HDFCBANK""]"
"selected = st.selectbox(""Select a Stock"", tickers)"

"if st.button(""Update Ticker""):"
"data_sheet.update(""A1"", selected)"

# Call your Apps Script web app to update Data!A1 formula
"apps_script_url = ""https://script.google.com/macros/s/AKfycbzBHt2lsU4N-6_Fx976L5oOq-pO7vSvxoPDaVN8z_yLVgsfdqqWUAoB-MyAConY-zl3_A/exec"""
try:
response = requests.get(apps_script_url)
if response.status_code == 200:
"st.success(f""Updated to {selected}. Loading live data..."")"
time.sleep(3)  # wait for GOOGLEFINANCE to fetch data
else:
"st.error(""Apps Script error"")"
except Exception as e:
"st.error(f""Request failed: {e}"")"

# === Fetch and display updated data ===
data = data_sheet.get_all_records()
if data:
df = pd.DataFrame(data)
"df[""Date""] = pd.to_datetime(df[""Date""])"
"st.line_chart(df.set_index(""Date"")[""Close""])  # Adjust if column is named differently"
