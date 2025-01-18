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
def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, contact, amenities, location_features, message):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    new_row = [
        name, dates, "NA", "NA", rent, unit_type, residence, address, contact, amenities, location_features, message, "Supply"
    ]
    sheet.append_row(new_row)

# Update contact details in Google Sheets
def update_contact_in_google_sheets(row, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    listings = sheet.get_all_records()

    # Ensure all keys are lowercased and stripped for comparison
    standardized_listings = [
        {key.lower().strip(): value for key, value in listing.items()}
        for listing in listings
    ]
    row_standardized = {key.lower().strip(): value for key, value in row.items()}

    # Identify row to update by matching key fields
    for i, listing in enumerate(standardized_listings):
        if (
            listing["name"].strip() == row_standardized["name"].strip()
            and listing["dates"].strip() == row_standardized["dates"].strip()
            and listing["address"].strip() == row_standardized["address"].strip()
        ):
            # Update "Contact" column
            contact_col_index = len(listing) - 3  # Adjust for "Contact" column index
            sheet.update_cell(i + 2, contact_col_index, contact)  # Add 2 to skip headers
            return True
    raise ValueError("Matching listing not found in Google Sheets.")






