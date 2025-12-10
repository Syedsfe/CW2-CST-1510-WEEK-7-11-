import streamlit as st

st.set_page_config(page_title="Week 9 Intelligence Platform", layout="wide")


# SESSION STATE INITIALIZATION

if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Register"     # ← Default when app loads


# AUTO REDIRECT WHEN LOGGED IN

if st.session_state.logged_in:
    st.switch_page("pages/1_Domain_Cybersecurity.py")



# HEADER
st.title("Multi-Domain Intelligence Platform")



# TABS (we control which one is shown using session_state)

if st.session_state.active_tab == "Register":
    tab_register, tab_login = st.tabs(["Register", "Login"])
else:
    tab_login, tab_register = st.tabs(["Login", "Register"])


# REGISTER TAB

with tab_register:
    st.subheader("Create New Account")

    new_user = st.text_input("Choose Username", key="new_user")
    new_pass = st.text_input("Choose Password", type="password", key="new_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")

    if st.button("Register Account"):
        if not new_user or not new_pass:
            st.warning("Please fill all fields.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created successfully! Please log in.")

            # Switch ACTIVE TAB → Login
            st.session_state.active_tab = "Login"
            st.rerun()   # Reload page so Login tab becomes active


# LOGIN TAB

with tab_login:
    st.subheader("Login")

    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log In"):
        if login_user in st.session_state.users and st.session_state.users[login_user] == login_pass:
            st.session_state.logged_in = True
            st.session_state.username = login_user
            st.success("Login successful!")
            st.rerun()   # Immediately redirects to Cybersecurity page
        else:
            st.error("Invalid username or password")
