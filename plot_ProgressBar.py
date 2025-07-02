import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def plotProgressBar(df):
    st.write("### 📈 Utility Relocation Progress by Station")
    
    
    df["Work Progress"] = pd.to_numeric(df["Work Progress"]) * 100
    df["Work Status (%)"] = df["Work Progress"].apply(lambda x: f"{x:.1f}%")
    df["Baseline Progress"] = pd.to_numeric(df["Baseline Progress"]) * 100
    df["Baseline Progress (%)"] = df["Baseline Progress"].apply(lambda x: f"{x:.1f}%")
    
    # Create columns (1:4 ratio)
    col1, col2 = st.columns([4, 11])
    
    with col1:
        
        # Load your image - Replace with your image path or URL
        project_image = Image.open("images/routeMap.jpg")
        
        # Display image with caption
        st.image(project_image, caption="Utility Relocation Route Map", use_container_width=True)

    with col2:
        # Create visualization
        fig, ax = plt.subplots(figsize=(14, 8), dpi=600)
        fig.patch.set_facecolor('#faf0e6')
        ax.set_facecolor('#faf0e6')
    
        # --- Original plotting code ---
        contract_packages = df["Contract Package"].unique()
        colors = plt.cm.Set1(range(len(contract_packages)))
        extra_legends = []
        bar_handles = []
    
        for i, package in enumerate(contract_packages):
            subset = df[df["Contract Package"] == package]
            baseline_bars = ax.barh(
                subset["Station Name"],
                subset["Baseline Progress"],
                color="#000",
                edgecolor="black",
                label="Baseline" if i == 0 else "",
                alpha=0.2,
                height=0.6
            )
            extra_legends.append(baseline_bars)
    
            current_bars = ax.barh(
                subset["Station Name"], 
                subset["Work Progress"], 
                color=colors[i], 
                label=package,
                height=0.4
            )
            bar_handles.append(current_bars)
            
            ax.bar_label(
                current_bars,
                labels=subset["Work Status (%)"],
                fontsize=9,
                padding=2,
                label_type="edge"
            )
    
        # Trendline
        y_pos = range(len(df))
        x_values = df["Work Progress"]
        trendline = ax.plot(
            x_values,
            y_pos,
            color="#FF4F0F",
            linestyle='-',
            marker='o',
            markersize=6,
            linewidth=1.5,
            alpha=0.7,
            label="Progress Trend"
        )
    
        extra_legends.append(trendline[0])
        clean_legends = [art for art in extra_legends if not art.get_label().startswith("_")]
    
        # Legends
        legend1 = ax.legend(
            handles=bar_handles,
            title="Contract Package",
            loc='upper left',
            bbox_to_anchor=(1.02, 1))
        ax.legend(
            handles=clean_legends,
            loc='upper left',
            bbox_to_anchor=(1.02, 0.75))
        ax.add_artist(legend1)
    
        # Labels and formatting
        ax.set_xlabel("Work Progress (%)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Station Name", fontsize=12, fontweight="bold")
        ax.set_title("Utility Relocation Progress by Station", fontsize=14, pad=20, fontweight="bold")
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_xlim(0, 107)
        plt.tight_layout()
        # --- End plotting code ---
    
        # Display in Streamlit
        st.pyplot(fig)
        
        # Optional: Show data table
        with st.expander("View Raw Data"):
            df_filtered = df.drop(columns=["Baseline Progress", "Work Progress"])
            st.dataframe(df_filtered)
