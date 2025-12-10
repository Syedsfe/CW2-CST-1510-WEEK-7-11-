import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def itops_analytics_ui():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()

    if df.empty:
        st.warning("No IT tickets available.")
        return

    # KPIs
    st.write("### 📌 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Tickets", df.shape[0])
    col2.metric("Open Tickets", df[df["status"] == "Open"].shape[0])

    st.write("---")

    # Priority distribution
    st.write("### ⚠️ Tickets by Priority")
    st.bar_chart(df["priority"].value_counts())

    st.write("---")

    # Status distribution
    st.write("### 📍 Tickets by Status")
    st.bar_chart(df["status"].value_counts())

    st.write("---")

    # Table preview
    st.write("### 📋 Ticket Details")
    st.dataframe(df)