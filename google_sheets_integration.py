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
        pd.Timestamp.now().strftime("%d/%m/%Y"),  # Date
        pd.Timestamp.now().strftime("%H:%M:%S"),  # Time
        name,                                     # Name
        dates,                                    # Dates
        "NA",                                     # Starting From
        "NA",                                     # Until
        rent,                                     # Rent
        unit_type,                                # Unit Type
        residence,                                # Residence
        address,                                  # Address
        amenities,                                # Amenities
        location_features,                        # Location Features
        message,                                  # Message
        contact,                                  # Contact
        "Supply"                                  # Classification
    ]
    sheet.append_row(new_row)

# Update contact details in Google Sheets
def update_contact_in_google_sheets(row, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1

    # Find the row index for the listing
    listings = sheet.get_all_records()
    for i, listing in enumerate(listings, start=2):  # Start at 2 to account for the header row
        if all(str(listing[key]).strip() == str(row[key]).strip() for key in row.index if key in listing):
            sheet.update_cell(i, len(listing) - 1, contact)  # Update the 'Contact' column
            break





