import streamlit as st
import pandas as pd
from google_sheets_integration import load_google_sheets, add_listing_to_google_sheets

# Load the Excel file
uploaded_file = "Filtered_WhatsApp_Announcements (1).xlsx"

sheets = {"All Messages": "All Messages", "Demands": "Demands", "Supply": "Supply"}
data = {name: pd.read_excel(uploaded_file, sheet_name=sheet) for name, sheet in sheets.items()}

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

    /* Call-to-action Buttons */
    .cta-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4a90e2;
        color: #ffffff;
        border-radius: 8px;
        text-decoration: none;
        text-align: center;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .cta-button:hover {
        background-color: #0076d5;
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

# Ensure proper sorting by Date, with NA values at the bottom
df_combined["Date"] = pd.to_datetime(df_combined["Date"], errors="coerce")
df_combined = df_combined.sort_values(by="Date", ascending=False, na_position="last")

# Sidebar filters
st.sidebar.header("Filters")
unit_type_filter = st.sidebar.selectbox("Filter by Unit Type:", options=["All"] + sorted(df_combined["Unit Type"].unique()))
residence_filter = st.sidebar.selectbox("Filter by Residence:", options=["All"] + sorted(df_combined["Residence"].unique()))

# Apply filters
if unit_type_filter != "All":
    df_combined = df_combined[df_combined["Unit Type"] == unit_type_filter]
if residence_filter != "All":
    df_combined = df_combined[df_combined["Residence"] == residence_filter]

# Display listings
st.title("Apartment Listings")

if not df_combined.empty:
    for _, row in df_combined.iterrows():
        title = "Residence" if row["Residence"] == "Yes" else "Accommodation"
        st.markdown(
            f"""
            <div class="card">
                <h4>{title}</h4>
                <p><strong>Dates:</strong> {row['Dates']}</p>
                <p><strong>Posted by:</strong> {row['Name']}</p>
                <p><strong>Posted on:</strong> {row['Date'].strftime('%d/%m/%Y') if not pd.isna(row['Date']) else 'NA'}</p>
                <p><strong>Location Features:</strong> {row['Location Features']}</p>
                <p class="price"><strong>Rent:</strong> {row['Rent']} €</p>
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
        # Add listing to Google Sheets
        add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message)
        st.success("Offer added successfully!")






















