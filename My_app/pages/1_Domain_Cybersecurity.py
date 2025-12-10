import streamlit as st

# IMPORT YOUR DOMAIN MODULES
from pages.cyber.crud import cyber_crud_ui
from pages.cyber.analytics import cyber_analytics_ui
from pages.cyber.ai_chat import cyber_ai_chat_ui

# PAGE CONFIG
st.set_page_config(page_title="Cybersecurity Intelligence", layout="wide")

# LOGIN CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# PAGE TITLE
st.title("🔐 Cybersecurity Intelligence Portal")
st.caption("Manage incidents, view analytics, and chat with the domain AI assistant.")

# CREATE THE 3 TABS
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

# TAB 1 — CRUD
with tab_crud:
    st.subheader("📁 Cybersecurity CRUD Operations")
    cyber_crud_ui()

# TAB 2 — ANALYTICS
with tab_analytics:
    st.subheader("📊 Cybersecurity Analytics Dashboard")
    cyber_analytics_ui()

# TAB 3 — AI CHAT
with tab_ai:
    st.subheader("🤖 Cybersecurity AI Assistant")
    st.caption("AI persona: Senior Cybersecurity Analyst.")
    cyber_ai_chat_ui()