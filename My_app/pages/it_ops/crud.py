import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def itops_crud_ui():
    st.subheader("🖥️ Manage IT Tickets")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New Ticket")

    issue = st.text_input("Issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    status = st.selectbox("Status", ["Open", "Closed"])

    if st.button("Add Ticket"):
        conn.execute("""
            INSERT INTO it_tickets (issue, priority, status)
            VALUES (?, ?, ?)
        """, (issue, priority, status))
        conn.commit()
        st.success("Ticket added!")
        st.experimental_rerun()

    st.write("---")
    st.write("### ✏️ Update Ticket")

    if df.shape[0] > 0:
        ticket_id = st.selectbox("Select ID to update", df["id"])

        new_issue = st.text_input("New Issue")
        new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"])
        new_status = st.selectbox("New New Status", ["Open", "Closed"])

        if st.button("Update Ticket"):
            conn.execute("""
                UPDATE it_tickets
                SET issue = ?, priority = ?, status = ?
                WHERE id = ?
            """, (new_issue, new_priority, new_status, ticket_id))
            conn.commit()
            st.success("Ticket updated!")
            st.experimental_rerun()

    st.write("---")
    st.write("### 🗑️ Delete Ticket")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select ID to delete", df["id"], key="delete_it")

        if st.button("Delete Ticket"):
            conn.execute("DELETE FROM it_tickets WHERE id = ?", (delete_id,))
            conn.commit()
            st.success("Ticket deleted!")
            st.experimental_rerun()

    conn.close()