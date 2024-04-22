import streamlit as st
from database import get_users


def login(username, password):
    if username == "admin" and password == "admin":
        st.session_state["logged_in"] = True
        st.session_state["role"] = "Admin"
        st.toast("Logged in successfully.")
    else:
        users = get_users()
        for user in users:
            if username == user[1]:
                st.session_state["logged_in"] = True
                st.session_state["role"] = "User"
                st.session_state["userid"] = user[0]
                st.toast("Logged in successfully.")
                break
        else:
            st.error("Incorrect username or password")


def show_login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Role Based Access Control
    st.button(":green[Login]", on_click=login, args=(username, password))
