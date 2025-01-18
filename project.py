import streamlit as st
import pandas as pd
from google_sheets_integration import load_google_sheets, add_listing_to_google_sheets, update_contact_in_google_sheets

# Loading the Excel file from previous part --> need to combine
uploaded_file = "Filtered_WhatsApp_Announcements.xlsx"
sheets = {"All Messages": "All Messages", "Demands": "Demands", "Supply": "Supply"}
data = {name: pd.read_excel(uploaded_file, sheet_name=sheet) for name, sheet in sheets.items()}

# Standardize column names in Excel data - have to match with google sheets
for key in data:
    data[key].columns = data[key].columns.str.strip().str.lower()

# Sidebar navigation to put in filters + others elements
st.sidebar.header("Navigation")
selected_view = st.sidebar.radio("Choose a view:", list(data.keys()))

# Put sheet into streamlit
df_excel = data[selected_view].fillna("NA")

# Load additional data from Google Sheets - source for additional offers.
st.write("Most recent offers")
df_google_sheets = load_google_sheets()

if not df_google_sheets.empty:
    # Standardizing column names in Google Sheets data
    df_google_sheets.columns = df_google_sheets.columns.str.strip().str.lower()

    # Combine datasets (excel + sheet)
    df_combined = pd.concat([df_excel, df_google_sheets], ignore_index=True)

    # Making sure dates correspond
    df_combined["date"] = pd.to_datetime(df_combined["date"], errors="coerce")
    df_combined["date"] = df_combined["date"].fillna("NA")

    # Sort by date, placing "NA" at the bottom (they are the ones we do not have information about)
    df_combined["sort_key"] = df_combined["date"].apply(lambda x: pd.Timestamp.min if x == "NA" else x)
    df_combined = df_combined.sort_values(by="sort_key", ascending=False).drop(columns=["sort_key"])

    # Format the "date" column for display
    df_combined["date_display"] = df_combined["date"].apply(
        lambda x: x.strftime("%d/%m/%Y") if x != "NA" else "NA"
    )

    # Sidebar filters with a toggle of all unique options
    st.sidebar.header("Filters")
    unit_type_filter = st.sidebar.selectbox(
        "Filter by Unit Type:", 
        options=["All"] + sorted(df_combined["unit type"].dropna().unique())
    )
    residence_filter = st.sidebar.selectbox(
        "Filter by Residence:", 
        options=["All", "Yes"]
    )

    # Filters apply to the selection
    if unit_type_filter != "All":
        df_combined = df_combined[df_combined["unit type"] == unit_type_filter]
    if residence_filter != "All":
        df_combined = df_combined[df_combined["residence"] == residence_filter]

    # Display listings corresponding sorted by most recent
    st.title("Apartment Listings (Sorted by Date Added)")

    if not df_combined.empty:
        for index, row in df_combined.iterrows():
            title = "Residence" if row["residence"] == "Yes" else "Accommodation"
            
            # Date display order
            if row['starting from'] != "NA" and row['until'] != "NA":
                date_display = f"From {row['starting from']} Until {row['until']}"
            elif row['starting from'] != "NA":
                date_display = f"From {row['starting from']}"
            elif row['until'] != "NA":
                date_display = f"Until {row['until']}"
            else:
                date_display = f"Dates: {row['dates']}"

            st.markdown(
                f"""
                <div class="card">
                    <h4>{title}</h4>
                    <p><strong>{date_display}</strong></p>
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
            # Add Contact Section for people to add contacts
            with st.expander(f"Add Contact to Listing {index}"):
                contact = st.text_input(f"Enter your contact details for listing {index}:")
                if st.button(f"Submit Contact for Listing {index}"):
                    if contact.strip():
                        update_contact_in_google_sheets(row, contact, index)
                        st.success(f"Contact added successfully for listing {index}!")
                    else:
                        st.error("Contact field cannot be empty.")
    else:
        st.write("No listings match your filters.")

else:
    st.error("Failed to load data from Google Sheets.")

# Sidebar form to add new listings - published to google sheets then downloaded back into streamlit
st.sidebar.header("Add a New Listing")
with st.sidebar.form("new_listing_form"):
    name = st.text_input("Name")
    contact = st.text_input("Contact (required)")
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
        if not contact.strip():
            st.error("Contact is required!")
        else:
            add_listing_to_google_sheets(name, dates, rent, unit_type, residence, address, amenities, location_features, message, contact)
            st.success("Offer added successfully!")


