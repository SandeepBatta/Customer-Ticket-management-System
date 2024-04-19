import streamlit as st
from src.login import show_login
from ticket import show_ticket_form, show_delete_ticket_form

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main app logic
if st.session_state["logged_in"]:
    show_ticket_form()
    show_delete_ticket_form()
else:
    show_login()
