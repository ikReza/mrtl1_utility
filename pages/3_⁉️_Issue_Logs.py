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

# Check for session persistence
if 'sheets' not in st.session_state or 'main_page' not in st.session_state:
    st.switch_page("Utility.py")

# Check authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

CORRECT_PASSCODE = st.secrets["passwords"]["my_pass"]

# Authentication gate
if not st.session_state.authenticated:
    st.title("Authentication Required 🔒")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=100)
    
    with col2:
        passcode = st.text_input("Enter passcode:", type="password")
        submit = st.button("Submit")

        if submit:
            if passcode == CORRECT_PASSCODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("⚠️ Incorrect passcode. Please try again.")
    
    st.stop()  # Stop execution if not authenticated

def issues():
    selected_station = st.session_state.get("selected_station", "No Station Selected")
    st.title(f"⌚ {selected_station.upper()} Station Issue Logs")
    
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