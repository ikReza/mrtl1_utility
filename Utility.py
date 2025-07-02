import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder
from plot_ProgressBar import plotProgressBar


st.set_page_config(
    page_title="Utility Relocation",
    page_icon="👋",
    layout="wide",
)

# Inject custom CSS to widen the main container and reduce padding
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define custom CSS for styling
custom_css = {
    ".ag-header": {  # Header background color
        "background-color": "#1f77b4",  # Blue header
        "color": "white",
        "font-size": "16px"
    },
    ".ag-row": {  # Row background color
        "background-color": "#f4f4f4"
    },
    ".ag-cell": {  # Cell text color
        "color": "#333"
    }
}

# Store current page path to handle reloads
if 'main_page' not in st.session_state:
    st.session_state.main_page = "Utility.py"

station_files = {
    "Natun Bazar": "s08_natun_bazar_progress.xlsx",
    "Aftab Nagar": "s05_aftab_nagar_progress.xlsx",
    "Badda": "s06_badda_progress.xlsx",
    "North Badda": "s07_north_badda_progress.xlsx"
}

st.sidebar.title("Select Station")
selected_station = st.sidebar.selectbox("Choose a Station", list(station_files.keys()))
st.sidebar.divider()

# Load data only when the station is changed
if "selected_station" not in st.session_state or st.session_state.selected_station != selected_station:
    st.session_state.selected_station = selected_station  # Store selection
    file_path = station_files[selected_station]  # Get corresponding file
    
    # Load all sheets from Excel file into a dictionary
    st.session_state.sheets = pd.read_excel(file_path, sheet_name=None)

progressFile = pd.read_excel("data/progress.xlsx")
plotProgressBar(progressFile)

def main():    
    sheets = st.session_state.sheets
    
    corridor_data = sheets["Corridor Work"]
    
    # Sidebar for corridor selection
    st.sidebar.title("Select Corridor")
    selected_corridor = st.sidebar.selectbox("Choose a corridor", corridor_data["Corridor"].unique())
    
    # Filter sections based on selected corridor
    sections_in_corridor = corridor_data[corridor_data["Corridor"] == selected_corridor]["Section"].unique()
    
    # Add "All" option if there are multiple sections
    if len(sections_in_corridor) > 1:
        sections_in_corridor = ["All"] + list(sections_in_corridor)
        
    selected_section = st.sidebar.selectbox("Choose a section", sections_in_corridor)
    
    # Filter data based on selected corridor and section
    if selected_section == "All":
        filtered_data = corridor_data[corridor_data["Corridor"] == selected_corridor]
    else:
        filtered_data = corridor_data[
            (corridor_data["Corridor"] == selected_corridor) &
            (corridor_data["Section"] == selected_section)
        ]
    
    # Display sections available for the selected corridor
    st.sidebar.write(f"**{selected_corridor} comprises the following sections:**")
    for section in sections_in_corridor:
        if section != "All":  # Skip "All" in the list
            st.sidebar.write(f"- Section - {section}")
    
    # Display work breakdown
    st.title(f"{selected_corridor}: Section-{selected_section} Work Progress")
    st.write("### Work Breakdown")
    
    filtered_data["Grouped Task"] = filtered_data["Task Group"].apply(
        lambda x: x if x == "Utility Laying" else f"{x}"
    )
    
    # Configure Ag-Grid
    gb = GridOptionsBuilder.from_dataframe(filtered_data)
    gb.configure_pagination(enabled=True)  # Enable pagination
    gb.configure_default_column(editable=False, groupable=True)
    gb.configure_column("Grouped Task", rowGroup=True, hide=True, rowGroupOpenByDefault=True)  # Group by this column
    gb.configure_column("Task Group", hide=True)  # Hide original task group column
    # Custom widths
    gb.configure_column("Progress (%)", hide=True)
    gb.configure_grid_options(domLayout='autoHeight')
    
    AgGrid(filtered_data, gridOptions=gb.build(), custom_css=custom_css, enable_enterprise_modules=True, height=600, theme="alpine")


if __name__ == "__main__":
    main()
    
footer_css = """
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            font-size: 14px;
            color: gray;
        }
    </style>
"""

# Display the footer with the creator's name
footer_text = '<p class="footer"><b>© July 2025</b></p>'

# Inject the CSS and HTML into Streamlit
st.markdown(footer_css, unsafe_allow_html=True)
st.markdown(footer_text, unsafe_allow_html=True)