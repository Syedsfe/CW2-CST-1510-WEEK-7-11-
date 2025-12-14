import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager

DB_PATH = "database/intelligence_platform.db"

def cyber_analytics_ui():
    db = DatabaseManager(DB_PATH)

    rows = db.fetch_all(
        "SELECT id, title, severity, status, date FROM cyber_incidents"
    )

    df = pd.DataFrame(rows, columns=["id", "title", "severity", "status", "date"])

    if df.empty:
        st.warning("No cyber incidents available.")
        return

    # Normalize for consistency
    df["severity"] = df["severity"].str.lower()
    df["status"] = df["status"].str.lower()

    st.write("### 📌 Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", df.shape[0])
    col2.metric("High Severity", df[df["severity"] == "high"].shape[0])
    col3.metric("Open Incidents", df[df["status"] == "open"].shape[0])

    st.write("---")

    st.write("### 🔥 Incidents by Severity")
    st.bar_chart(df["severity"].value_counts())

    st.write("---")

    st.write("### 📍 Open vs Closed Incidents")
    st.bar_chart(df["status"].value_counts())

    st.write("---")

    st.write("### 📅 Incidents Over Time")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    st.line_chart(df.groupby("date").size())
