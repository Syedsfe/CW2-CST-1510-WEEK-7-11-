import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def cyber_crud_ui():
    st.subheader("🔐 Manage Cyber Incidents")

    conn = sqlite3.connect(DB_PATH)

    # READ incidents
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New Incident")

    title = st.text_input("Incident Title")
    severity = st.selectbox("Severity", ["High", "Medium", "Low"])
    status = st.selectbox("Status", ["Open", "Closed"])
    date = st.date_input("Date")

    if st.button("Add Incident"):
        conn.execute("""
            INSERT INTO cyber_incidents (title, severity, status, date)
            VALUES (?, ?, ?, ?)
        """, (title, severity, status, str(date)))
        conn.commit()
        st.success("Incident added successfully!")
        st.experimental_rerun()

    st.write("---")
    st.write("### ✏️ Update Incident")

    if df.shape[0] > 0:
        incident_id = st.selectbox("Select ID to update", df["id"])

        new_title = st.text_input("New Title")
        new_severity = st.selectbox("New Severity", ["High", "Medium", "Low"])
        new_status = st.selectbox("New Status", ["Open", "Closed"])

        if st.button("Update Incident"):
            conn.execute("""
                UPDATE cyber_incidents
                SET title = ?, severity = ?, status = ?
                WHERE id = ?
            """, (new_title, new_severity, new_status, incident_id))
            conn.commit()
            st.success("Incident updated!")
            st.experimental_rerun()

    st.write("---")
    st.write("### 🗑️ Delete Incident")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select ID to delete", df["id"], key="delete_cyber")

        if st.button("Delete Incident"):
            conn.execute("DELETE FROM cyber_incidents WHERE id = ?", (delete_id,))
            conn.commit()
            st.success("Incident deleted!")
            st.experimental_rerun()

    conn.close()