import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.security_incidents import SecurityIncident

DB_PATH = "database/intelligence_platform.db"

def cyber_crud_ui():
    st.subheader("🔐 Manage Cyber Incidents (OOP Refactor)")

    db = DatabaseManager(DB_PATH)

    # -----------------------------
    # READ INCIDENTS INTO OBJECTS
    # -----------------------------
    rows = db.fetch_all("SELECT id, title, severity, status, date FROM cyber_incidents")

    incidents = [
        SecurityIncident(
            incident_id=row[0],
            title=row[1],
            severity=row[2],
            status=row[3],
            date=row[4]
        )
        for row in rows
    ]

    # Convert to DataFrame for UI
    df = pd.DataFrame([
        {
            "ID": i.get_id(),
            "Title": i.get_title(),
            "Severity": i.get_severity(),
            "Severity Level": i.get_severity_level(),
            "Status": i.get_status(),
            "Date": i.get_date()
        }
        for i in incidents
    ])

    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New Incident")

    title = st.text_input("Incident Title")
    severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
    status = st.selectbox("Status", ["open", "closed"])
    date = st.date_input("Date")

    if st.button("Add Incident"):
        db.execute_query(
            """
            INSERT INTO cyber_incidents (title, severity, status, date)
            VALUES (?, ?, ?, ?)
            """,
            (title, severity.lower(), status, str(date))
        )
        st.success("Incident added successfully!")
        st.rerun()

    st.write("---")
    st.write("### ✏️ Update Incident")

    if df.shape[0] > 0:
        incident_id = st.selectbox("Select ID to update", df["ID"])

        new_title = st.text_input("New Title")
        new_severity = st.selectbox("New Severity", ["low", "medium", "high", "critical"])
        new_status = st.selectbox("New Status", ["open", "closed"])

        if st.button("Update Incident"):
            db.execute_query(
                """
                UPDATE cyber_incidents
                SET title = ?, severity = ?, status = ?
                WHERE id = ?
                """,
                (new_title, new_severity.lower(), new_status, incident_id)
            )
            st.success("Incident updated!")
            st.rerun()

    st.write("---")
    st.write("### 🗑️ Delete Incident")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select ID to delete", df["ID"], key="delete_cyber")

        if st.button("Delete Incident"):
            db.execute_query(
                "DELETE FROM cyber_incidents WHERE id = ?",
                (delete_id,)
            )
            st.success("Incident deleted!")
            st.rerun()
