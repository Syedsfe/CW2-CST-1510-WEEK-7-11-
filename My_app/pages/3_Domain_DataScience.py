import streamlit as st

# IMPORT DOMAIN MODULES
from pages.datasci.crud import datasci_crud_ui
from pages.datasci.analytics import datasci_analytics_ui
from pages.datasci.ai_chat import datasci_ai_chat_ui

# PAGE CONFIG
st.set_page_config(page_title="Data Science Intelligence", layout="wide")

# LOGIN CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# PAGE TITLE
st.title("📊 Data Science Intelligence Portal")
st.caption("Manage datasets, explore analytics, and chat with the data science AI assistant.")

# CREATE THE 3 TABS
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

# TAB 1 — CRUD
with tab_crud:
    st.subheader("📁 Dataset Metadata CRUD Operations")
    datasci_crud_ui()

# TAB 2 — ANALYTICS
with tab_analytics:
    st.subheader("📊 Data Science Analytics Dashboard")
    datasci_analytics_ui()

# TAB 3 — AI CHAT
with tab_ai:
    st.subheader("🤖 Data Science AI Assistant")
    st.caption("AI persona: Senior Data Scientist.")
    datasci_ai_chat_ui()