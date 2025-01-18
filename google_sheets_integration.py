import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Load data from Google Sheets
def load_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        try:
            sheet = client.open("Listing_form").sheet1
        except gspread.SpreadsheetNotFound:
    st.error("Spreadsheet 'Listing_form' not found. Check the name.")

        data = sheet.get_all_records()
        if not data:
            st.warning("Google Sheet is empty or has no records.")
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading Google Sheets: {e}")
        return pd.DataFrame()

# Add a new listing to Google Sheets
def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message, contact):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Listing_form").sheet1
        new_row = [
            pd.Timestamp.now().strftime("%d/%m/%Y"),  # Date
            pd.Timestamp.now().strftime("%H:%M:%S"),  # Time
            name, dates, "NA", "NA", rent, unit_type, residence, address, amenities, location_features, message, contact, "Supply"
        ]
        sheet.append_row(new_row)
    except Exception as e:
        st.error(f"Error adding listing: {e}")

# Update contact details in Google Sheets
def update_contact_in_google_sheets(row, contact, index):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Listing_form").sheet1

        listings = sheet.get_all_records()
        sheet.update_cell(index + 2, len(listings[0]), contact)  # Update the contact column for the correct row
    except Exception as e:
        st.error(f"Error updating contact: {e}")


