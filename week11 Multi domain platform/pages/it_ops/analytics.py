import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager

DB_PATH = "database/intelligence_platform.db"   # Corrected DB path

def itops_analytics_ui():

    db = DatabaseManager(DB_PATH)

    # Load tickets using OOP DB manager
    rows = db.fetch_all("""
        SELECT id, title, priority, status, created_date
        FROM it_tickets
    """)

    df = pd.DataFrame(
        rows,
        columns=["id", "title", "priority", "status", "created_date"]
    )

    if df.empty:
        st.warning("No IT tickets available.")
        return

    # Normalize values for consistent casing
    df["priority"] = df["priority"].str.lower()
    df["status"] = df["status"].str.lower()

    # ------------------------
    # KPIs
    # ------------------------
    st.write("### 📌 Summary Metrics")

    col1, col2 = st.columns(2)
    col1.metric("Total Tickets", df.shape[0])
    col2.metric("Open Tickets", df[df["status"] == "open"].shape[0])

    st.write("---")

    # ------------------------
    # Priority distribution
    # ------------------------
    st.write("### ⚠️ Tickets by Priority")
    st.bar_chart(df["priority"].value_counts())

    st.write("---")

    # ------------------------
    # Status distribution
    # ------------------------
    st.write("### 📍 Tickets by Status")
    st.bar_chart(df["status"].value_counts())

    st.write("---")

    # ------------------------
    # Created Date Timeline
    # ------------------------
    st.write("### 🕒 Ticket Creation Over Time")

    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df_valid = df.dropna(subset=["created_date"])

    timeline = df_valid.groupby("created_date").size()
    st.line_chart(timeline)

    st.write("---")

    # ------------------------
    # Table preview
    # ------------------------
    st.write("### 📋 Ticket Details Table")
    st.dataframe(df, use_container_width=True)
