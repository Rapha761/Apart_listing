import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Load data from Google Sheets
def load_google_sheets():
    # Authenticate using Streamlit Secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Listing_form").sheet1

    # Fetch data
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Add a new listing to Google Sheets
def add_listing_to_google_sheets(name, rent, unit_type, residence, location_features):
    # Authenticate using Streamlit Secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Listing_form").sheet1

    # Append new data
    sheet.append_row([name, rent, unit_type, residence, location_features])

