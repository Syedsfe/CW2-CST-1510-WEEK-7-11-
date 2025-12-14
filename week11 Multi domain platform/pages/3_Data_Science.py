import streamlit as st

# Import your modular UI components
from pages.datasci.crud import datasci_crud_ui
from pages.datasci.analytics import datasci_analytics_ui
from pages.datasci.ai_chat import datasci_ai_chat_ui

# Page configuration
st.set_page_config(page_title="Data Science Intelligence", layout="wide")

# Login guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# Page Title
st.title("📊 Data Science Intelligence Portal")
st.caption("Manage datasets, view analytics, and chat with the Data Science AI assistant.")

# Create tabs for the domain components
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

# CRUD Tab
with tab_crud:
    st.subheader("📁 Dataset CRUD Operations")
    datasci_crud_ui()

# Analytics Tab
with tab_analytics:
    st.subheader("📊 Dataset Analytics Dashboard")
    datasci_analytics_ui()

# AI Chat Tab
with tab_ai:
    st.subheader("🤖 Data Science AI Assistant")
    st.caption("AI persona: Senior Data Scientist.")
    datasci_ai_chat_ui()
