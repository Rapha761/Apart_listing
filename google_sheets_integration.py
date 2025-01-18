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

    # Ensure all keys and values are lowercased and stripped for comparison
    standardized_listings = [
        {key.lower().strip(): str(value).strip() for key, value in listing.items()}
        for listing in listings
    ]
    row_standardized = {key.lower().strip(): str(value).strip() for key, value in row.items()}

    # Debugging: Log row and listings for comparison
    print("Standardized Row:", row_standardized)
    print("Standardized Listings:", standardized_listings)

    # Identify row to update by matching key fields
    for i, listing in enumerate(standardized_listings):
        try:
            if (
                listing.get("name", "") == row_standardized.get("name", "")
                and listing.get("dates", "") == row_standardized.get("dates", "")
                and listing.get("address", "") == row_standardized.get("address", "")
            ):
                # Update "Contact" column
                contact_col_index = list(sheet.get_all_records()[0].keys()).index("Contact") + 1  # Adjust for 'Contact'
                sheet.update_cell(i + 2, contact_col_index, contact)  # Add 2 to skip header
                print(f"Contact successfully updated for row {i + 2}")
                return True
        except Exception as e:
            print(f"Error during contact update for row {i + 2}: {e}")
            continue

    # Debugging: If no match is found
    print("Matching listing not found for:", row_standardized)
    raise ValueError("Matching listing not found in Google Sheets.")




