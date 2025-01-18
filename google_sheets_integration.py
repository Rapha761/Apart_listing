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
        # Fetch all values from the sheet
        raw_data = sheet.get_all_values()

        # Check if the sheet has any rows
        if not raw_data or len(raw_data) < 2:
            st.warning("Google Sheet is empty or has no data.")
            return pd.DataFrame()

        # Extract headers and rows
        headers = raw_data[0]
        rows = raw_data[1:]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)

        # Fill missing columns with "NA" for consistency
        df = df.fillna("NA")

        st.write(f"Loaded {len(df)} rows from Google Sheets.")
        return df

    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
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
        # Fetch all records and standardize for comparison
        records = sheet.get_all_records()
        records_df = pd.DataFrame(records)
        records_df.columns = records_df.columns.str.lower().str.strip()

        # Standardize the input row for comparison
        row_standardized = {key.lower().strip(): str(value).strip().lower() for key, value in row.items()}

        # Find the matching row in Google Sheets
        for i, listing in records_df.iterrows():
            if (listing.to_dict() == row_standardized):
                # Update the "Contact" column
                sheet.update_cell(i + 2, list(records[0].keys()).index("Contact") + 1, contact)
                st.success("Contact updated successfully!")
                return

        raise ValueError("Matching listing not found in Google Sheets.")

    except Exception as e:
        st.error(f"Error updating contact: {e}")
        raise


