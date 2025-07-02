import streamlit as st
import pandas as pd
import plotly.express as px

from plot_sCurve import plotSCurve
from plot_Agency import plotAgencyBar, plotCivilWork

st.set_page_config(page_title="Plotting", page_icon="📈", layout="wide")

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

station_files = {
    "Aftab Nagar": "s05_aftab_nagar_progress.xlsx",
    "Nadda": "nadda_progress.xlsx",
    "Natun Bazar": "s08_natun_bazar_progress.xlsx",
    "Badda": "badda_progress.xlsx",
    "Rampura": "rampura_progress.xlsx",
    "Malibagh": "malibagh_progress.xlsx"
}

st.sidebar.title("Select Station")
selected_station = st.sidebar.selectbox("Choose a Station", list(station_files.keys()))
st.sidebar.divider()

if "selected_station" not in st.session_state or st.session_state.selected_station != selected_station:
    st.session_state.selected_station = selected_station  # Store selection
    file_path = station_files[selected_station]  # Get corresponding file
    
    # Load all sheets from Excel file into a dictionary
    st.session_state.sheets = pd.read_excel(file_path, sheet_name=None)

def plot():
    selected_station = st.session_state.get("selected_station", "No Station Selected")
    st.title(f"📌 Station: {selected_station.upper()}")
    
    sheets = st.session_state.sheets
    df = sheets["Corridor Work"]
    
    # Grouping Data by Corridor (East vs. West)
    target_columns = ["Planned", "Actual"]
    east_work = df.loc[df["Corridor"] == "East", target_columns].sum()
    west_work = df.loc[df["Corridor"] == "West", target_columns].sum()
    total_work = df[target_columns].sum()
    
    # Create Summary DataFrame for Bar Chart 1
    summary_df = pd.DataFrame({
        "Category": ["East Side", "West Side", "Total Work"],
        "Planned": [east_work["Planned"], west_work["Planned"], total_work["Planned"]],
        "Actual": [east_work["Actual"], west_work["Actual"], total_work["Actual"]]
    })
    
    # Calculate Percentage for Actual Work
    summary_df["Actual %"] = (summary_df["Actual"] / summary_df["Planned"]) * 100  # Compute progress %
    
    # Convert to string with % symbol for display
    summary_df["Actual % Text"] = summary_df["Actual %"].apply(lambda x: f"{x:.1f}%")
    
    # Grouping Data by Identifier (Main Road vs. Secondary Road)
    road_summary = df.groupby(["Identifier", "Corridor"])[["Planned", "Actual"]].sum().reset_index()
    # Calculate Percentage for Actual Work
    road_summary["Actual %"] = (road_summary["Actual"] / road_summary["Planned"]) * 100  # Compute progress %
    
    # Convert to string with % symbol for display
    road_summary["Actual % Text"] = road_summary["Actual %"].apply(lambda x: f"{x:.1f}%")
    
    # Streamlit App Layout
    #st.title("📊 Work Progress Visualization")
    
    # First Bar Chart: East Side vs. West Side vs. Total Work
    st.write("### 🏗️ Work Progress by Corridor (East vs. West)")
    fig1 = px.bar(summary_df, x="Category", y=["Planned", "Actual"], 
                  barmode="group", title="Planned vs. Actual Work Progress by Corridor",
                  labels={"value": "Work Volume", "Category": "Corridor"})

    # fig1.update_layout(plot_bgcolor='#faf0e6').update_layout(paper_bgcolor='#faf0e6')
    
    # Add Percentage Text on the Actual Bars
    for i, bar in enumerate(fig1.data):
        if bar.name == "Actual":  # Only add percentage to the "Actual" bars
            bar.text = summary_df["Actual % Text"]  # Assign formatted percentages
            bar.textposition = "outside"  # Show text above bars
            
    # Customize layout: Add border & make legend bigger
    fig1.update_layout(
        plot_bgcolor="#faf0e6",  # White background
        paper_bgcolor="#faf0e6",
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for space
        legend=dict(font=dict(size=14, color="black")),
        xaxis=dict(showgrid=False, zeroline=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=True, zeroline=False),  # Keep y-axis grid for readability
        font=dict(color='#000000'),
        shapes=[
            dict(
                type="rect",  # Rectangle border
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,  # Full size
                line=dict(color="black", width=2)  # Black border
            )
        ]
    )
    
    st.plotly_chart(fig1)
    
sheets = st.session_state.sheets
      
plot()
plotSCurve(sheets["Progress"])
plotAgencyBar(sheets["Corridor Work"])
plotCivilWork(sheets["Corridor Work"])