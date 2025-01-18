import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd


def load_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)


def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    new_row = [
        name, dates, "NA", "NA", rent, unit_type, residence, address, amenities, location_features, message, "NA", "Supply"
    ]
    sheet.append_row(new_row)


def update_contact_in_google_sheets(name, dates, address, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    data = sheet.get_all_records()

    for i, row in enumerate(data):
        if row["Name"] == name and row["Dates"] == dates and row["Address"] == address:
            sheet.update_cell(i + 2, list(row.keys()).index("Contact") + 1, contact)
            return

    raise ValueError("Matching listing not found in Google Sheets.")


