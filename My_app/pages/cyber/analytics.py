import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def cyber_analytics_ui():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()

    if df.empty:
        st.warning("No cyber incidents available.")
        return

    # Summary KPIs
    st.write("### 📌 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", df.shape[0])
    col2.metric("High Severity", df[df["severity"] == "High"].shape[0])
    col3.metric("Open Incidents", df[df["status"] == "Open"].shape[0])

    st.write("---")

    # Severity chart
    st.write("### 🔥 Incidents by Severity")
    st.bar_chart(df["severity"].value_counts())

    # Status chart
    st.write("### 📍 Open vs Closed Incidents")
    st.bar_chart(df["status"].value_counts())

    st.write("---")

    # Incidents per date (if available)
    if "date" in df.columns:
        st.write("### 📅 Incidents Over Time")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        date_counts = df.groupby("date").size()
        st.line_chart(date_counts)