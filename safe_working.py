import streamlit as st
import pandas as pd

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
df = data[selected_view]

# Replace NaN with "NA"
df = df.fillna("NA")

# Sidebar filters
st.sidebar.header("Filters")
unit_type_filter = st.sidebar.selectbox("Filter by Unit Type:", options=["All"] + sorted(df["Unit Type"].unique()))
residence_filter = st.sidebar.selectbox("Filter by Residence:", options=["All"] + sorted(df["Residence"].unique()))

# Apply filters
if unit_type_filter != "All":
    df = df[df["Unit Type"] == unit_type_filter]
if residence_filter != "All":
    df = df[df["Residence"] == residence_filter]

# Display listings
st.title("Apartment Listings")

if not df.empty:
    for _, row in df.iterrows():
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

# Example CTA button
st.markdown(
    '<a class="cta-button" href="#">Submit a Listing</a>',
    unsafe_allow_html=True,
)
