import streamlit as st

# Import domain UI modules
from pages.it_ops.crud import itops_crud_ui
from pages.it_ops.analytics import itops_analytics_ui
from pages.it_ops.ai_chat import itops_ai_chat_ui

# Page config
st.set_page_config(page_title="IT Operations Intelligence", layout="wide")

# Login guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# Title and description
st.title("🖥️ IT Operations Intelligence Portal")
st.caption("Manage IT tickets, view operational analytics, and chat with the IT Ops AI assistant.")

# Tabs for each module
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

with tab_crud:
    st.subheader("📁 IT Ticket CRUD Operations")
    itops_crud_ui()

with tab_analytics:
    st.subheader("📊 IT Operations Analytics Dashboard")
    itops_analytics_ui()

with tab_ai:
    st.subheader("🤖 IT Operations AI Assistant")
    st.caption("AI persona: IT Support / DevOps Engineer.")
    itops_ai_chat_ui()
