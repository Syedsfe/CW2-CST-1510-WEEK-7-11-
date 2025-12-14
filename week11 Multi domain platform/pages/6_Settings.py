import streamlit as st
from services.database_manager import DatabaseManager

st.set_page_config(page_title="Settings", layout="wide")

# LOGIN GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# PAGE TITLE
st.title("⚙️ Settings")
st.caption("Manage app preferences, AI chat history, and account options.")

st.divider()

# ---------------------------------------------------------
# USER INFORMATION
# ---------------------------------------------------------
st.subheader("👤 User Information")

st.write(f"**Logged in as:** `{st.session_state.username}`")
st.write(f"**Role:** `user`")  # If you want roles later, you can update here.

st.divider()

# ---------------------------------------------------------
# AI HISTORY RESET SECTION
# ---------------------------------------------------------
st.subheader("🧹 Clear AI Chat Histories")

col1, col2, col3, col4 = st.columns(4)

if col1.button("Clear Cybersecurity Chat"):
    st.session_state.cyber_ai_history = []
    st.success("Cybersecurity AI chat history cleared!")

if col2.button("Clear Data Science Chat"):
    st.session_state.ds_ai_history = []
    st.success("Data Science AI chat history cleared!")

if col3.button("Clear IT Ops Chat"):
    st.session_state.it_ai_history = []
    st.success("IT Ops AI chat history cleared!")

if col4.button("Clear General AI Assistant"):
    if "general_ai" in st.session_state:
        st.session_state.general_ai.clear_history()
    st.success("General AI Assistant chat history cleared!")

st.divider()

# ---------------------------------------------------------
# THEME SETTINGS (STREAMLIT NATIVE)
# ---------------------------------------------------------
st.subheader("🎨 Theme Settings")

theme = st.radio(
    "Choose Theme",
    ["Light", "Dark"],
    index=0
)

st.info("Note: Theme will be applied after refreshing the page (Streamlit limitation).")

st.divider()

# ---------------------------------------------------------
# OPTIONAL — DATABASE RESET (DEV ONLY)
# ---------------------------------------------------------
st.subheader("🗄 Database Tools (Optional)")

dev_mode = st.checkbox("Enable developer database reset tools")

if dev_mode:
    db = DatabaseManager("database/intelligence_platform.db")

    if st.button("Reset ALL Tables (Dangerous)"):
        st.warning("Resetting database tables...")
        db.execute_query("DELETE FROM cyber_incidents")
        db.execute_query("DELETE FROM datasets_metadata")
        db.execute_query("DELETE FROM it_tickets")
        st.success("All tables cleared!")

st.divider()

# ---------------------------------------------------------
# LOGOUT BUTTON
# ---------------------------------------------------------
st.subheader("🔐 Logout")

if st.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.switch_page("pages/1_Login.py")

st.divider()

# ---------------------------------------------------------
# ABOUT SECTION
# ---------------------------------------------------------
st.subheader("ℹ️ About This Application")

st.write("""
This Multi-Domain Intelligence Platform is built using:

- **Streamlit** (UI framework)  
- **SQLite** (Database)  
- **OpenAI GPT-4o-mini** (AI backend)  
- **Custom OOP Architecture** (Week 11 refactor)  
- Multi-domain intelligence modules:
  - Cybersecurity  
  - Data Science  
  - IT Operations  
  - Central AI Assistant  
""")
