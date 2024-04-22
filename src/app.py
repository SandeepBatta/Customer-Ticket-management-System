import streamlit as st
from login import show_login
from home import home

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main app logic
if not st.session_state["logged_in"]:
    show_login()
else:
    home()
