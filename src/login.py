import streamlit as st
from database import get_users,insert_user


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

def show_signup_form():
    st.session_state["signup"] = True
    st.session_state["logged_in"] = True

def signup():
    st.subheader("Signup")
    first_name = st.text_input("First Name", key="signup_firstname")
    last_name = st.text_input("Last Name", key="signup_lastname")
    name = first_name + " " + last_name
    email = st.text_input("Email", key="signup_email")
    age = st.text_input("Age", key="signup_age")
    gender = st.text_input("Gender", key="signup_gender")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        insert_user(
            name,
            email,
            age,
            gender,
        )
        st.toast("user created successfully.")

def show_login_form():
    st.session_state["logged_in"] = False
    st.session_state["signup"] = False