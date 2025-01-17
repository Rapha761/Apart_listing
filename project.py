import streamlit as st
import pandas as pd
from google_sheets_integration import load_google_sheets, add_listing_to_google_sheets


# Load the Excel file
uploaded_file = "Filtered_WhatsApp_Announcements (1).xlsx"

sheets = {"All Messages": "All Messages", "Demands": "Demands", "Supply": "Supply"}
data = {name: pd.read_excel(uploaded_file, sheet_name=sheet) for name, sheet in sheets.items()}

# Sidebar navigation
st.sidebar.header("Navigation")
selected_view = st.sidebar.radio("Choose a view:", list(data.keys()))

# Load the selected sheet
df_excel = data[selected_view].fillna("NA")

# Load additional data from Google Sheets
df_google_sheets = load_google_sheets()

# Combine both datasets
df_combined = pd.concat([df_excel, df_google_sheets], ignore_index=True)

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
                <p><strong>Posted on:</strong> {row['Date']}</p>
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
    rent = st.number_input("Rent (€)", min_value=0, step=50)
    unit_type = st.selectbox("Unit Type", ["Studio", "Apartment", "Room"])
    residence = st.radio("Residence", ["Yes", "No"])
    location_features = st.text_area("Location Features")
    submit = st.form_submit_button("Add Offer")

    if submit:
        add_listing_to_google_sheets(name, rent, unit_type, residence, location_features)
        st.success("Offer added successfully!")




















