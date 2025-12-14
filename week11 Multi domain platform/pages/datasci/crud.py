import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.dataset import Dataset

DB_PATH = "database/intelligence_platform.db"   # your real db file

def datasci_crud_ui():

    st.subheader("📊 Manage Dataset Metadata (OOP Refactor)")

    db = DatabaseManager(DB_PATH)

    # --------------------------
    # Load datasets into objects
    # --------------------------
    rows = db.fetch_all("""
        SELECT id, dataset_name, category, source, last_updated, record_count, file_size_mb
        FROM datasets_metadata
    """)

    datasets = [
        Dataset(
            dataset_id=row[0],
            name=row[1],
            category=row[2],
            source=row[3],
            last_updated=row[4],
            record_count=row[5],
            file_size_mb=row[6]
        )
        for row in rows
    ]

    # Display table
    df = pd.DataFrame([
        {
            "ID": d.get_id(),
            "Name": d.get_name(),
            "Category": d.get_category(),
            "Source": d.get_source(),
            "Last Updated": d.get_last_updated(),
            "Records": d.get_row_count(),
            "Size (MB)": d.get_size_mb()
        }
        for d in datasets
    ])

    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.write("### ➕ Add New Dataset")

    name = st.text_input("Dataset Name")
    category = st.text_input("Category (e.g., Finance, Health, Transport)")
    source = st.text_input("Source (URL, File, API)")
    last_updated = st.date_input("Last Updated")
    record_count = st.number_input("Record Count", min_value=0)
    file_size_mb = st.number_input("File Size (MB)", min_value=0.0)

    if st.button("Add Dataset"):
        db.execute_query("""
            INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, source, str(last_updated), record_count, file_size_mb))

        st.success("Dataset added!")
        st.rerun()

    st.write("---")
    st.write("### ✏️ Update Dataset")

    if df.shape[0] > 0:
        dataset_id = st.selectbox("Select Dataset to Update", df["ID"])

        new_name = st.text_input("New Name")
        new_category = st.text_input("New Category")
        new_source = st.text_input("New Source")
        new_record_count = st.number_input("New Record Count", min_value=0)
        new_file_size = st.number_input("New File Size (MB)", min_value=0.0)

        if st.button("Update Dataset"):
            db.execute_query("""
                UPDATE datasets_metadata
                SET dataset_name = ?, category = ?, source = ?, record_count = ?, file_size_mb = ?
                WHERE id = ?
            """, (new_name, new_category, new_source, new_record_count, new_file_size, dataset_id))

            st.success("Dataset updated!")
            st.rerun()

    st.write("---")
    st.write("### 🗑️ Delete Dataset")

    if df.shape[0] > 0:
        delete_id = st.selectbox("Select Dataset to Delete", df["ID"], key="delete_ds")

        if st.button("Delete Dataset"):
            db.execute_query("DELETE FROM datasets_metadata WHERE id = ?", (delete_id,))
            st.success("Dataset deleted!")
            st.rerun()
