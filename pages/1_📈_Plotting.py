import streamlit as st
import pandas as pd
import plotly.express as px

from plot_sCurve import plotSCurve
from plot_Agency import plotAgencyBar, plotCivilWork

st.set_page_config(page_title="Plotting", page_icon="📈")

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

def plot():
    sheets = st.session_state.sheets
    df = sheets["Corridor Work"]
    
    # Grouping Data by Corridor (East vs. West)
    east_work = df[df["Corridor"] == "East"].sum()
    west_work = df[df["Corridor"] == "West"].sum()
    total_work = df.sum()
    
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
    print(road_summary)
    
    # Streamlit App Layout
    st.title("📊 Work Progress Visualization")
    
    # First Bar Chart: East Side vs. West Side vs. Total Work
    st.write("### 🏗️ Work Progress by Corridor (East vs. West)")
    fig1 = px.bar(summary_df, x="Category", y=["Planned", "Actual"], 
                  barmode="group", title="Planned vs. Actual Work Progress by Corridor",
                  labels={"value": "Work Volume", "Category": "Corridor"})
    
    # Add Percentage Text on the Actual Bars
    for i, bar in enumerate(fig1.data):
        if bar.name == "Actual":  # Only add percentage to the "Actual" bars
            bar.text = summary_df["Actual % Text"]  # Assign formatted percentages
            bar.textposition = "outside"  # Show text above bars
            
    # Customize layout: Add border & make legend bigger
    fig1.update_layout(
        plot_bgcolor="white",  # White background
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for space
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        legend=dict(font=dict(size=14)),
        xaxis=dict(showgrid=False, zeroline=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=True, zeroline=False),  # Keep y-axis grid for readability
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
    
    
if __name__ == "__main__":
    plot()
    plotSCurve()
    plotAgencyBar()
    plotCivilWork()