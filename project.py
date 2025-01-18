import streamlit as st
import pandas as pd
from google_sheets_integration import load_google_sheets, add_listing_to_google_sheets

# Load the Excel file
uploaded_file = "Filtered_WhatsApp_Announcements (7).xlsx"

sheets = {"All Messages": "All Messages", "Demands": "Demands", "Supply": "Supply"}
data = {name: pd.read_excel(uploaded_file, sheet_name=sheet) for name, sheet in sheets.items()}

# Standardize column names in Excel data
for key in data:
    data[key].columns = data[key].columns.str.strip().str.lower()

# Global styles
st.markdown(
    """
    <style>
    /* Background for Sidebar */
    [data-testid="stSidebar"] {
        background-color: #e6f3ff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar Toggle Buttons */
    [data-testid="stSidebar"] .css-1d391kg {
        border-radius: 20px;
        background-color: #ffffff;
        padding: 8px 16px;
        margin-bottom: 5px;
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stSidebar"] .css-1d391kg:hover {
        background-color: #4a90e2;
        color: #ffffff;
    }
    [data-testid="stSidebar"] .css-1d391kg[aria-selected="true"] {
        background-color: #0076d5;
        color: #ffffff;
    }

    /* Filter Dropdown Styling */
    .css-1wxaqej {
        border: 1px solid #cccccc;
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Card Styling */
    .card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    .card:hover {
        background-color: #f0f8ff;
        border-color: #0076d5;
    }

    /* Text Styling */
    h4 {
        color: #333333;
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 24px;
    }
    p {
        color: #555555;
        font-family: 'Helvetica', sans-serif;
        font-size: 16px;
        line-height: 1.5;
    }
    .price {
        color: #0076d5;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
st.sidebar.header("Navigation")
selected_view = st.sidebar.radio("Choose a view:", list(data.keys()))

# Load the selected sheet
df_excel = data[selected_view].fillna("NA")

# Load additional data from Google Sheets
df_google_sheets = load_google_sheets()

# Combine both datasets
df_combined = pd.concat([df_excel, df_google_sheets], ignore_index=True)

# Parse the "date", "starting from", and "until" columns
for column in ["date", "starting from", "until"]:
    df_combined[column] = pd.to_datetime(df_combined[column], errors="coerce")

# Replace invalid dates with "NA"
df_combined["starting from"] = df_combined["starting from"].fillna("NA")
df_combined["until"] = df_combined["until"].fillna("NA")
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
unit_type_filter = st.sidebar.selectbox("Filter by Unit Type:", options=["All"] + sorted(df_combined["unit type"].unique()))
residence_filter = st.sidebar.selectbox("Filter by Residence:", options=["All"] + sorted(df_combined["residence"].unique()))
date_range = st.sidebar.date_input("Filter by Dates (Start and End):", [])

# Apply filters
if unit_type_filter != "All":
    df_combined = df_combined[df_combined["unit type"] == unit_type_filter]
if residence_filter != "All":
    df_combined = df_combined[df_combined["residence"] == residence_filter]

# Filter based on "Starting From" and "Until"
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

    # Inclusive logic with 2-month buffers
    buffer_start_date = start_date - pd.Timedelta(days=60)
    buffer_end_date = end_date + pd.Timedelta(days=60)

    # Create masks for filtering
    mask_starting_from = (df_combined["starting from"] <= buffer_end_date) | (df_combined["starting from"] == "NA")
    mask_until = (df_combined["until"] >= buffer_start_date) | (df_combined["until"] == "NA")

    # Apply the masks
    df_combined = df_combined[mask_starting_from & mask_until]

# Display listings
st.title("Apartment Listings (Sorted by Date Added)")

if not df_combined.empty:
    for _, row in df_combined.iterrows():
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
            </div>
            """,
            unsafe_allow_html=True,
        )
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



