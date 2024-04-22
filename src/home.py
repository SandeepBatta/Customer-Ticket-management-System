import streamlit as st
from ticket import show_create_ticket, show_tickets


def home():
    if not st.session_state["logged_in"]:
        st.error("Please login to view this page.")
        st.stop()

    def clear_session_state():
        keys = list(st.session_state.keys())
        for key in keys:
            st.session_state.pop(key)

    with st.sidebar:
        st.button(":red[Logout]", on_click=clear_session_state)

    _, col2 = st.columns(2)

    # Column 2: Create Ticket on the top right
    with col2:
        with st.expander("Create Ticket"):
            show_create_ticket()

    show_tickets()
