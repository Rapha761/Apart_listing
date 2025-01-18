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
def add_listing_to_google_sheets(
    name, contact, dates, rent, unit_type, residence, address, amenities, location_features, message
):
    # Authenticate using Streamlit Secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Listing_form").sheet1

    # Define the row to append, matching the column order in the sheet
    new_row = [
        pd.Timestamp.now().strftime("%d/%m/%Y"),  # Date (current date)
        pd.Timestamp.now().strftime("%H:%M:%S"),  # Time (current time)
        name,  # Name (user input)
        dates,  # Dates (user input)
        "NA",  # Starting From (default value)
        "NA",  # Until (default value)
        rent,  # Rent (user input)
        unit_type,  # Unit Type (user input)
        residence,  # Residence (user input)
        address,  # Address (user input)
        amenities,  # Amenities (user input)
        location_features,  # Location Features (user input)
        message,  # Message (user input)
        contact,  # Contact (user input)
        "Supply",  # Classification (default value)
    ]

    # Append the new row to the sheet
    sheet.append_row(new_row)







