import streamlit as st
import pandas as pd
import plotly.express as px

def plotAgencyBar(df):
    st.write("### 📈 Agency-wise Bar Chart")
    
    # --- Filter Data: Only include Utility Laying rows ---
    df_utility = df[df["Task Group"].str.lower() == "utility laying"]
    
    grouped = df_utility.groupby(["Corridor", "Work Breakdown", "Size"], as_index=False).agg({
                "Planned": "sum",
                "Actual": "sum"
            })
    
    # Calculate the completion percentage for each group.
    grouped["Completion (%)"] = (grouped["Actual"] / grouped["Planned"]) * 100
    
    # --- Create Custom Labels ---
    # For each Corridor and Work Breakdown, if there are multiple rows (i.e. multiple Sizes), append the Size.
    grouped["Label"] = None  # initialize label column
    
    for (corr, wb), sub in grouped.groupby(["Corridor", "Work Breakdown"]):
        if sub.shape[0] > 1:
            # Multiple entries for the same agency in the corridor: append Size.
            labels = sub["Work Breakdown"] + " (" + sub["Size"] + ")"
        else:
            # Only one entry: use just the agency name.
            labels = sub["Work Breakdown"]
        grouped.loc[sub.index, "Label"] = labels
    
    # --- Plotting: Separate Bar Charts for East and West ---
    east_data = grouped[grouped["Corridor"] == "East"]
    west_data = grouped[grouped["Corridor"] == "West"]
    
    color_map = {
        "DWASA": "skyblue",
        "DNCC Drainage": "seagreen",
        "TITAS": "magenta",
        "BTCL": "crimson",
        "Pvt. Communication Cable": "coral"  # Add other agencies as needed.
    }
    
    def plot_chart(data, corridor):
        fig = px.bar(
            data,
            x="Label",
            y="Completion (%)",
            text="Completion (%)",
            title=f"{corridor} Corridor: Completion Percentage by Task Group",
            labels={"Label": "Task Breakdown", "Completion (%)": "Completion (%)"},
            color="Work Breakdown",
            color_discrete_map=color_map
        )
        # Format text to one decimal place and position above bars. # Ensure text is not clipped
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', cliponaxis=False)
        fig.update_layout(
            plot_bgcolor="white",  # White background
            legend=dict(font=dict(size=14)),
            
        )
        return fig
    
    fig_east = plot_chart(east_data, "East")
    fig_west = plot_chart(west_data, "West")
    
    st.plotly_chart(fig_east)
    st.plotly_chart(fig_west)

def plotCivilWork(df):
    st.write("### 🛣️ Civil Work Bar Chart")
    
    df_filtered = df[df["Task Group"].isin(["Excavation", "Road Reinstatement"])].copy()
    
    # --- Group by Corridor, Task Group, and Work Breakdown ---
    df_grouped = (
        df_filtered.groupby(["Corridor", "Task Group", "Work Breakdown"], as_index=False, sort=False)
        .agg({"Planned": "sum", "Actual": "sum"})
    )
    
    # --- Compute Completion Percentage ---
    df_grouped["Completion (%)"] = (df_grouped["Actual"] / df_grouped["Planned"]) * 100

    # --- Create Combined Rows ---
    # For each (Corridor, Task Group) combination, compute the overall (combined) Planned and Actual.
    combined = (
        df_grouped.groupby(["Corridor", "Task Group"], as_index=False)
        .agg({"Planned": "sum", "Actual": "sum"})
    )
    combined["Work Breakdown"] = "Combined"  # Label these rows as Combined
    combined["Completion (%)"] = (combined["Actual"] / combined["Planned"]) * 100
    
    # --- Combine the Detailed and Overall Data ---
    df_combined = pd.concat([df_grouped, combined], ignore_index=True)
    
    # --- Separate Data for Each Corridor ---
    east_df = df_combined[df_combined["Corridor"] == "East"]
    west_df = df_combined[df_combined["Corridor"] == "West"]
    
    color_map = {
        "Road Reinstatement": "skyblue",
        "Excavation": "coral",
        "Pavement Cutting": "#FF9C6E",
        "Excavation Combined": "#E84118",
    }
    
    # --- Plotting Function ---
    def plot_chart(data, corridor):
        fig = px.bar(
            data,
            x="Work Breakdown",
            y="Completion (%)",
            text="Completion (%)",
            title=f"{corridor} Corridor: Completion Percentage by Task Group",
            labels={"Work Breakdown": "Task Breakdown", "Completion (%)": "Completion (%)"},
            color="Task Group",
            color_discrete_map=color_map,
            barmode="group"
        )
        # Format text to one decimal place and position above bars.
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', cliponaxis=False)
        fig.update_layout(
            plot_bgcolor="white",  # White background
            legend=dict(font=dict(size=14)),
            bargap=0,  # Reduce space between bars (default is 0.2)
            xaxis=dict(tickangle=-45),
        )
        return fig
    
    fig_east = plot_chart(east_df, "East")
    fig_west = plot_chart(west_df, "West")
    
    st.plotly_chart(fig_east)
    st.plotly_chart(fig_west)