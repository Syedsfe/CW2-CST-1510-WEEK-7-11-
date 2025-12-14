import streamlit as st
from services.auth_manager import AuthManager
from services.database_manager import DatabaseManager

# PAGE CONFIG
st.set_page_config(page_title="Login | Multi-Domain Intelligence Platform", layout="centered")

# CREATE DATABASE + AUTH MANAGER
db = DatabaseManager("database/intelligence_platform.db")
auth = AuthManager(db)

# SESSION DEFAULTS
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Login"

# IF LOGGED IN → GO TO HOME PAGE
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.switch_page("pages/0_home.py")

# PAGE HEADER
st.title("🔐 Login to Multi-Domain Intelligence Platform")

# TAB CONTROL
tab_login, tab_register = st.tabs(["Login", "Register"])

# ---------------------------------
# LOGIN TAB
# ---------------------------------
with tab_login:
    st.subheader("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        user = auth.login_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user.get_username()

            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password.")

# ---------------------------------
# REGISTER TAB
# ---------------------------------
with tab_register:
    st.subheader("Create New Account")

    new_user = st.text_input("Choose Username", key="reg_user")
    new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register Account"):
        if new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            created = auth.register_user(new_user, new_pass)

            if created:
                st.success("Account created successfully! Please log in.")
                st.session_state.active_tab = "Login"
                st.rerun()
            else:
                st.error("Username already exists or registration failed.")
