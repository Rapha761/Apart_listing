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
    data = sheet.get_all_records()
    return pd.DataFrame(data)

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
    listings = sheet.get_all_records()

    standardized_listings = [
        {key.lower().strip(): str(value).strip() for key, value in listing.items()}
        for listing in listings
    ]
    row_standardized = {key.lower().strip(): str(value).strip() for key, value in row.items()}

    for i, listing in enumerate(standardized_listings):
        if (
            listing.get("name", "") == row_standardized.get("name", "")
            and listing.get("dates", "") == row_standardized.get("dates", "")
            and listing.get("address", "") == row_standardized.get("address", "")
        ):
            sheet.update_cell(i + 2, list(listings[0].keys()).index("contact") + 1, contact)
            return
    raise ValueError("Matching listing not found in Google Sheets.")




