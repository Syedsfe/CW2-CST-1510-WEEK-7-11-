import streamlit as st

# Import domain components
from pages.cyber.crud import cyber_crud_ui
from pages.cyber.analytics import cyber_analytics_ui
from pages.cyber.ai_chat import cyber_ai_chat_ui

# Page configuration
st.set_page_config(page_title="Cybersecurity Intelligence", layout="wide")

# Login guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# Page Title
st.title("🛡 Cybersecurity Intelligence Portal")
st.caption("Manage cyber incidents, explore analytics, and chat with the Cybersecurity AI Assistant.")

# Create three tabs for the domain
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

# --- CRUD TAB ---
with tab_crud:
    st.subheader("📁 Cyber Incident CRUD Operations")
    cyber_crud_ui()

# --- ANALYTICS TAB ---
with tab_analytics:
    st.subheader("📊 Cybersecurity Analytics Dashboard")
    cyber_analytics_ui()

# --- AI CHAT TAB ---
with tab_ai:
    st.subheader("🤖 Cybersecurity AI Assistant")
    st.caption("AI persona: Senior Cybersecurity Analyst.")
    cyber_ai_chat_ui()
