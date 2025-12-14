import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.it_tickets import ITTicket

DB_PATH = "database/intelligence_platform.db"  # Correct DB path

def itops_crud_ui():
    st.subheader("🖥️ Manage IT Tickets (OOP Refactor)")

    db = DatabaseManager(DB_PATH)

    # -----------------------------
    # Load tickets into OOP objects
    # -----------------------------
    rows = db.fetch_all("""
        SELECT id, title, priority, status, created_date
        FROM it_tickets
    """)

    tickets = [
        ITTicket(
            ticket_id=row[0],
            title=row[1],
            priority=row[2],
            status=row[3],
            assigned_to="N/A"  # your table does not yet support this
        )
        for row in rows
    ]

    # Convert to DataFrame
    df = pd.DataFrame([
        {
            "ID": t.get_id(),
            "Title": t._ITTicket__title,
            "Priority": t._ITTicket__priority,
            "Status": t.get_status(),
            "Created Date": row[4]
        }
        for t, row in zip(tickets, rows)
    ])

    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New IT Ticket")

    title = st.text_input("Issue Title")
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    status = st.selectbox("Status", ["open", "closed"])
    created_date = st.date_input("Created Date")

    if st.button("Add Ticket"):
        db.execute_query("""
            INSERT INTO it_tickets (title, priority, status, created_date)
            VALUES (?, ?, ?, ?)
        """, (title, priority, status, str(created_date)))

        st.success("Ticket added successfully!")
        st.rerun()

    st.write("---")
    st.write("### ✏️ Update Ticket")

    if df.shape[0] > 0:
        ticket_id = st.selectbox("Select Ticket ID to Update", df["ID"])

        new_title = st.text_input("New Title")
        new_priority = st.selectbox("New Priority", ["low", "medium", "high"])
        new_status = st.selectbox("New Status", ["open", "closed"])

        if st.button("Update Ticket"):
            db.execute_query("""
                UPDATE it_tickets
                SET title = ?, priority = ?, status = ?
                WHERE id = ?
            """, (new_title, new_priority, new_status, ticket_id))

            st.success("Ticket updated!")
            st.rerun()

    st.write("---")
    st.write("### 🗑️ Delete Ticket")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select Ticket ID to Delete", df["ID"], key="delete_it")

        if st.button("Delete Ticket"):
            db.execute_query(
                "DELETE FROM it_tickets WHERE id = ?",
                (delete_id,)
            )
            st.success("Ticket deleted successfully!")
            st.rerun()
