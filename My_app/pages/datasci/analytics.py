import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def datasci_analytics_ui():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()

    if df.empty:
        st.warning("No dataset metadata available.")
        return

    # Summary KPIs
    st.write("### 📌 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Datasets", df.shape[0])
    col2.metric("Avg File Size (MB)", round(df["file_size_mb"].mean(), 2))
    col3.metric("Total Records", df["record_count"].sum())

    st.write("---")

    # Category distribution
    st.write("### 📂 Datasets by Category")
    st.bar_chart(df["category"].value_counts())

    # File sizes
    st.write("### 💾 File Size Distribution (MB)")
    st.bar_chart(df["file_size_mb"])

    st.write("---")

    # Last updated timeline
    if "last_updated" in df.columns:
        st.write("### 🕒 Dataset Updates Over Time")
        df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
        timeline = df.groupby("last_updated").size()
        st.line_chart(timeline)