import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import datetime

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
    df = pd.DataFrame(data)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()
    return df

def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message):
    # Authenticate using Streamlit Secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Listing_form").sheet1

    # Define the row to append, matching the column order in the sheet
    new_row = [
        datetime.now().strftime("%Y-%m-%d"),  # Date (current date)
        datetime.now().strftime("%H:%M:%S"),  # Time (current time)
        name,                                 # Name (user input)
        dates,                                # Dates (user input)
        "",                                   # Starting from (default empty)
        "",                                   # Until (default empty)
        rent,                                 # Rent (user input)
        unit_type,                            # Unit type (user input)
        residence,                            # Residence (user input)
        address,                              # Address (user input)
        amenities or "NA",                    # Amenities (user input, optional)
        location_features or "NA",            # Location features (user input, optional)
        message or "NA",                      # Message (user input, optional)
        "Offering",                           # Classification (default: Offering)
    ]

    # Append the new row to the sheet
    sheet.append_row(new_row)





