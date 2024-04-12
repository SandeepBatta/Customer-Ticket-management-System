import streamlit as st

def show_login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "admin":  # Simple check (replace with real authentication)
            st.session_state['logged_in'] = True
            st.success("Logged in successfully.")
        else:
            st.error("Incorrect username or password")
