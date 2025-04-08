import streamlit as st
import pandas as pd
import plotly.express as px

def plotSCurve(df):
    st.write("### 📈 Progress S-Curve")
    sheets = st.session_state.sheets
    df = sheets["Progress"]
    
    # Stop the actual work progress curve at 8th March
    cutoff_date = pd.Timestamp("2025-03-08")
    df.loc[df["Date"] > cutoff_date, "Actual"] = None
    
    fig = px.line(df, x="Date", y=["Baseline", "Actual"],
                  labels={"value": "Cumulative Work (%)", "Date": "Date"},
                  title="Cumulative Work Progress vs. Baseline",
                  color_discrete_map={"Baseline": "black", "Actual": "red"})    
    
    for trace in fig.data:
        if trace.name == "Baseline":
            #trace.line.dash = "dash"   # dot/dash for Baseline
            trace.line.dash = "4,2"
            trace.line.width = 4
        elif trace.name == "Actual":
            trace.line.dash = "solid"  # Solid for Actual
            trace.line.width = 4
    fig.update_xaxes(tickangle=90, dtick=604800000, showgrid=True, gridcolor="lightgray")  # 7 days in milliseconds
    fig.update_yaxes(rangemode="tozero") # Force the y-axis to start at 0
    fig.update_layout(height=700,
                      legend=dict(font=dict(size=16)),
                      shapes=[
                          dict(
                              type="rect",  # Rectangle border
                              xref="paper", yref="paper",
                              x0=0, y0=0, x1=1, y1=1,  # Full size
                              line=dict(color="black", width=2)  # Black border
                          )
                      ])

    st.plotly_chart(fig)