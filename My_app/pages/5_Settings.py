import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

# AUTH GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to access settings.")
    st.stop()

st.title("⚙️ Settings")
st.caption("Manage your account preferences, theme, and application settings.")

st.write("---")

# USER ACCOUNT SETTINGS
st.subheader("👤 Account Settings")

st.write(f"**Logged in as:** `{st.session_state.username}`")

new_username = st.text_input("Change Username", value=st.session_state.username)
new_password = st.text_input("Change Password", type="password")

if st.button("Update Account"):
    if new_username.strip() == "" or new_password.strip() == "":
        st.error("Both fields are required.")
    else:
        st.session_state.users[new_username] = new_password
        # Remove the old username
        if new_username != st.session_state.username:
            st.session_state.users.pop(st.session_state.username)
        st.session_state.username = new_username
        st.success("Account updated successfully!")

st.write("---")


# THEME SETTINGS
st.subheader("🎨 Theme Preferences")
theme_choice = st.radio("Choose theme:", ["Dark Mode", "Light Mode"], index=0)
st.info("Note: Custom themes require Streamlit Cloud or theme configuration in `.streamlit/config.toml`.")
st.write("---")

# APPLICATION ACTIONS
st.subheader("🚪 Logout")

if st.button("Log Out"):
    st.session_state.logged_in = False
    st.success("You have been logged out.")
    st.switch_page("home.py")