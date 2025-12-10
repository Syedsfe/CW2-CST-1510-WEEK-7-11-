import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "intelligence_platform.db"

def datasci_crud_ui():
    st.subheader("📊 Manage Dataset Metadata")

    conn = sqlite3.connect(DB_PATH)

    # READ datasets
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New Dataset")

    name = st.text_input("Dataset Name")
    file_type = st.selectbox("File Type", ["CSV", "Excel", "JSON", "Database"])
    rows = st.number_input("Rows", min_value=0, step=1)

    if st.button("Add Dataset"):
        conn.execute("""
            INSERT INTO datasets_metadata (name, file_type, rows)
            VALUES (?, ?, ?)
        """, (name, file_type, rows))
        conn.commit()
        st.success("Dataset added!")
        st.experimental_rerun()

    st.write("---")
    st.write("### ✏️ Update Dataset")

    if df.shape[0] > 0:
        dataset_id = st.selectbox("Select ID to update", df["id"])

        new_name = st.text_input("New Name")
        new_type = st.selectbox("New File Type", ["CSV", "Excel", "JSON", "Database"])
        new_rows = st.number_input("New Rows", min_value=0, step=1)

        if st.button("Update Dataset"):
            conn.execute("""
                UPDATE datasets_metadata
                SET name = ?, file_type = ?, rows = ?
                WHERE id = ?
            """, (new_name, new_type, new_rows, dataset_id))
            conn.commit()
            st.success("Dataset updated!")
            st.experimental_rerun()

    st.write("---")
    st.write("### 🗑️ Delete Dataset")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select ID to delete", df["id"], key="delete_ds")

        if st.button("Delete Dataset"):
            conn.execute("DELETE FROM datasets_metadata WHERE id = ?", (delete_id,))
            conn.commit()
            st.success("Dataset deleted!")
            st.experimental_rerun()

    conn.close()