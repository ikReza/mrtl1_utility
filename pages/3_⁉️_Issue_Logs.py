import streamlit as st
import pandas as pd

st.set_page_config(page_title="Issue Logs", page_icon="⁉️", layout="wide")

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

def issues():
    st.title("Issue Page")
    st.write("Welcome to the issue logs page!")
    
    sheets = st.session_state.sheets
    
    df = sheets["Issue Log"]
    # Format the date columns
    if "Created on" in df.columns:
        df["Created on"] = pd.to_datetime(df["Created on"]).dt.strftime("%d-%b-%Y")
    if 'Resolved on' in df.columns:
        df["Resolved on"] = pd.to_datetime(df["Resolved on"]).dt.strftime("%d-%b-%Y")
    
    st.dataframe(df, hide_index=True)
    
if __name__ == "__main__":
    issues()