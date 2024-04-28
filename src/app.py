import streamlit as st
from login import show_login, show_signup_form,signup,show_login_form
from home import home

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["signup"] = False

# Main app logic
if not st.session_state["logged_in"]:
    show_login()
    st.write("New user?")
    st.button("Go to Sign Up", on_click=show_signup_form)

elif st.session_state["signup"] :
    signup()
    st.button("Back to Login", on_click=show_login_form)

else:
    home()

