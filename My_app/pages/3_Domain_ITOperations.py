import streamlit as st

# IMPORT DOMAIN MODULES
from pages.it_ops.crud import itops_crud_ui
from pages.it_ops.analytics import itops_analytics_ui
from pages.it_ops.ai_chat import itops_ai_chat_ui

# PAGE CONFIG
st.set_page_config(page_title="IT Operations Intelligence", layout="wide")

# LOGIN CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please log in first.")
    st.stop()

# PAGE TITLE
st.title("🖥️ IT Operations Intelligence Portal")
st.caption("Manage IT tickets, view operational analytics, and chat with the IT Ops AI assistant.")

# CREATE THE 3 TABS
tab_crud, tab_analytics, tab_ai = st.tabs(["CRUD", "Analytics", "AI Chat"])

# TAB 1 — CRUD
with tab_crud:
    st.subheader("📁 IT Ticket CRUD Operations")
    itops_crud_ui()


# TAB 2 — ANALYTICS
with tab_analytics:
    st.subheader("📊 IT Operations Analytics Dashboard")
    itops_analytics_ui()

# TAB 3 — AI CHAT
with tab_ai:
    st.subheader("🤖 IT Operations AI Assistant")
    st.caption("AI persona: IT Support / DevOps Engineer.")
    itops_ai_chat_ui()