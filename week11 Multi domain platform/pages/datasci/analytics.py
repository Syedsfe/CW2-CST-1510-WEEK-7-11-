import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager

DB_PATH = "database/intelligence_platform.db"   # corrected path

def datasci_analytics_ui():
    db = DatabaseManager(DB_PATH)

    # Fetch dataset metadata using OOP DB Manager
    rows = db.fetch_all("""
        SELECT id, dataset_name, category, source, last_updated, record_count, file_size_mb
        FROM datasets_metadata
    """)

    df = pd.DataFrame(
        rows,
        columns=["id", "dataset_name", "category", "source", "last_updated", "record_count", "file_size_mb"]
    )

    if df.empty:
        st.warning("No dataset metadata available.")
        return

    st.write("### 📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Datasets", df.shape[0])
    col2.metric("Avg File Size (MB)", round(df["file_size_mb"].mean(), 2))
    col3.metric("Total Records", df["record_count"].sum())

    st.write("---")

    # 📂 Category distribution
    st.write("### 📂 Datasets by Category")
    st.bar_chart(df["category"].value_counts())

    st.write("---")

    # 💾 File size distribution
    st.write("### 💾 File Size Distribution (MB)")
    st.bar_chart(df["file_size_mb"])

    st.write("---")

    # 🕒 Last updated timeline
    st.write("### 🕒 Dataset Updates Over Time")

    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    df = df.dropna(subset=["last_updated"])  # remove invalid dates

    timeline = df.groupby("last_updated").size()
    st.line_chart(timeline)
