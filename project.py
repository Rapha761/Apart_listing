import streamlit as st
import pandas as pd
from google_sheets_integration import load_google_sheets, add_listing_to_google_sheets, update_contact_in_google_sheets

# Load the Excel file
uploaded_file = "Filtered_WhatsApp_Announcements (9).xlsx"
sheets = {"All Messages": "All Messages", "Demands": "Demands", "Supply": "Supply"}
data = {name: pd.read_excel(uploaded_file, sheet_name=sheet) for name, sheet in sheets.items()}

# Standardize column names in Excel data
for key in data:
    data[key].columns = data[key].columns.str.strip().str.lower()

# Sidebar navigation
st.sidebar.header("Navigation")
selected_view = st.sidebar.radio("Choose a view:", list(data.keys()))

# Load the selected sheet
df_excel = data[selected_view].fillna("NA")

# Load additional data from Google Sheets
df_google_sheets = load_google_sheets()

# Standardize column names in Google Sheets data
df_google_sheets.columns = df_google_sheets.columns.str.strip().str.lower()

# Combine datasets
df_combined = pd.concat([df_excel, df_google_sheets], ignore_index=True)

# Parse the "date" column and handle errors
df_combined["date"] = pd.to_datetime(df_combined["date"], errors="coerce")
df_combined["date"] = df_combined["date"].fillna("NA")

# Sort by date, placing "NA" at the bottom
df_combined["sort_key"] = df_combined["date"].apply(lambda x: pd.Timestamp.min if x == "NA" else x)
df_combined = df_combined.sort_values(by="sort_key", ascending=False).drop(columns=["sort_key"])

# Format the "date" column for display
df_combined["date_display"] = df_combined["date"].apply(
    lambda x: x.strftime("%d/%m/%Y") if x != "NA" else "NA"
)

# Sidebar filters
st.sidebar.header("Filters")
unit_type_filter = st.sidebar.selectbox(
    "Filter by Unit Type:", 
    options=["All"] + sorted(df_combined["unit type"].dropna().unique())
)
residence_filter = st.sidebar.selectbox(
    "Filter by Residence:", 
    options=["All", "Yes"]
)

# Apply filters
if unit_type_filter != "All":
    df_combined = df_combined[df_combined["unit type"] == unit_type_filter]
if residence_filter != "All":
    df_combined = df_combined[df_combined["residence"] == residence_filter]

# Display listings
st.title("Apartment Listings (Sorted by Date Added)")

if not df_combined.empty:
    for index, row in df_combined.iterrows():
        title = "Residence" if row["residence"] == "Yes" else "Accommodation"
        st.markdown(
            f"""
            <div class="card">
                <h4>{title}</h4>
                <p><strong>Dates:</strong> {row['dates']}</p>
                <p><strong>Posted by:</strong> {row['name']}</p>
                <p><strong>Posted on:</strong> {row['date_display']} at {row['time'] if row['time'] != 'NA' else 'NA'}</p>
                <p><strong>Address:</strong> {row['address']}</p>
                <p><strong>Amenities:</strong> {row['amenities']}</p>
                <p><strong>Location Features:</strong> {row['location features']}</p>
                <p class="price"><strong>Rent:</strong> {row['rent']} €</p>
                <p><strong>Message:</strong> {row['message']}</p>
                <p><strong>Contact:</strong> {row['contact']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Add Contact to Listing {index}"):
            contact = st.text_input("Enter your contact details:")
            if st.button("Submit Contact"):
                update_contact_in_google_sheets(row, contact)
                st.success("Contact added successfully!")
else:
    st.write("No listings match your filters.")

# Sidebar form to add new listings
st.sidebar.header("Add a New Listing")
with st.sidebar.form("new_listing_form"):
    name = st.text_input("Name")
    dates = st.text_input("Dates (e.g., '01 Jan 2025 - 31 Jan 2025')")
    address = st.text_input("Address")
    rent = st.number_input("Rent (€)", min_value=0, step=50)
    unit_type = st.selectbox("Unit Type", ["Studio", "Apartment", "Room"])
    residence = st.radio("Residence", ["Yes", "No"])
    amenities = st.text_area("Amenities (optional)")
    location_features = st.text_area("Location Features (optional)")
    message = st.text_area("Message (optional)")
    submit = st.form_submit_button("Add Offer")

    if submit:
        add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message)
        st.success("Offer added successfully!")



