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
def add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    new_row = [
        name, dates, "NA", "NA", rent, unit_type, residence, address, amenities, location_features, message, "NA", "Supply"
    ]
    sheet.append_row(new_row)

# Update contact details in Google Sheets
def update_contact_in_google_sheets(row, contact):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1
    data = sheet.get_all_records()

    # Match the row using its unique fields
    for i, listing in enumerate(data):
        if (listing["Name"] == row["name"] and
            listing["Dates"] == row["dates"] and
            listing["Address"] == row["address"]):
            # Update the contact column
            sheet.update_cell(i + 2, list(listing.keys()).index("Contact") + 1, contact)
            return
    raise ValueError("Matching listing not found in Google Sheets.")

# Transfer Excel data to Google Sheets (with duplicate prevention)
def transfer_excel_to_google_sheets(df_excel):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open("Listing_form").sheet1

    # Load existing data from Google Sheets
    existing_data = sheet.get_all_records()

    # Append new rows if they don't exist
    for _, row in df_excel.iterrows():
        if not any(
            listing["Name"] == row["name"] and
            listing["Dates"] == row["dates"] and
            listing["Address"] == row["address"]
            for listing in existing_data
        ):
            new_row = [
                str(row["name"]), 
                str(row["dates"]), 
                str(row.get("starting from", "NA")),
                str(row.get("until", "NA")),
                str(row["rent"]), 
                str(row["unit type"]),
                str(row["residence"]), 
                str(row["address"]), 
                str(row.get("amenities", "NA")),
                str(row.get("location features", "NA")), 
                str(row.get("message", "NA")),
                str(row.get("contact", "NA")), 
                "Supply"
            ]
            sheet.append_row(new_row)

