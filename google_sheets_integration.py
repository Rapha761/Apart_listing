import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Load data from Google Sheets
def load_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1

    try:
        # Fetch records from the Google Sheet
        data = sheet.get_all_records()
        st.write(f"Google Sheet loaded successfully. Found {len(data)} rows.")
        return pd.DataFrame(data)
    except Exception as e:
        # Debugging raw data
        st.error(f"Error loading Google Sheet: {e}")
        st.write("Attempting to fetch raw values for debugging...")
        raw_values = sheet.get_all_values()
        st.write(f"Raw values from Google Sheets: {raw_values}")
        raise

# Add a new listing to Google Sheets
def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    new_row = [
        name, dates, "NA", "NA", rent, unit_type, residence, address, amenities, location_features, message, contact, "Supply"
    ]
    sheet.append_row(new_row)

# Update contact details in Google Sheets
def update_contact_in_google_sheets(row, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1

    try:
        # Find the matching row in Google Sheets
        records = sheet.get_all_records()
        for i, record in enumerate(records):
            if (record.get("Name", "").strip().lower() == row["name"].strip().lower() and
                record.get("Dates", "").strip().lower() == row["dates"].strip().lower()):
                # Update the "Contact" column
                sheet.update_cell(i + 2, list(record.keys()).index("Contact") + 1, contact)
                st.success("Contact updated successfully!")
                return

        raise ValueError("Matching listing not found in Google Sheets.")
    except Exception as e:
        st.error(f"Error updating contact: {e}")
        raise

