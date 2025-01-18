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
            try:
                sheet.append_row(new_row)
            except Exception as e:
                st.error(f"Error adding row: {e}")
