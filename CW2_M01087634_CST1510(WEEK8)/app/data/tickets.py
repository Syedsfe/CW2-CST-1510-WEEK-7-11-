import pandas as pd
from pathlib import Path
import sqlite3

# Relative import so it works with: python3 -m app.data.tickets
from .db import connect_database

DATA_DIR = Path("DATA")


# -------------------------
# CRUD FUNCTIONS
# -------------------------

def insert_ticket(conn: sqlite3.Connection, title: str, priority: str,
                  status: str = "open", created_date: str = None):
    """
    Insert a new IT ticket and return its new id.
    Matches schema:
    it_tickets(id, title, priority, status, created_date)
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
        """,
        (title, priority, status, created_date)
    )
    conn.commit()
    return cursor.lastrowid


def get_ticket_by_id(conn: sqlite3.Connection, ticket_id: int):
    """Fetch one ticket by id."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE id = ?", (ticket_id,))
    return cursor.fetchone()


def get_all_tickets(conn: sqlite3.Connection):
    """Fetch all tickets."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets ORDER BY id DESC")
    return cursor.fetchall()


def update_ticket(conn: sqlite3.Connection, ticket_id: int,
                  title=None, priority=None, status=None, created_date=None):
    """
    Update ticket fields if provided.
    """
    current = get_ticket_by_id(conn, ticket_id)
    if not current:
        return False

    new_title = title if title is not None else current[1]
    new_priority = priority if priority is not None else current[2]
    new_status = status if status is not None else current[3]
    new_created_date = created_date if created_date is not None else current[4]

    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE it_tickets
        SET title = ?, priority = ?, status = ?, created_date = ?
        WHERE id = ?
        """,
        (new_title, new_priority, new_status, new_created_date, ticket_id)
    )
    conn.commit()
    return True


def delete_ticket(conn: sqlite3.Connection, ticket_id: int):
    """Delete a ticket by id."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount


# -------------------------
# CSV LOADING (Checklist)
# -------------------------

def load_it_tickets_csv(conn: sqlite3.Connection, csv_filename="it_tickets_1000.csv"):
    """
    Load IT tickets from CSV into it_tickets table.
    CSV columns expected: id, title, priority, status, created_date

    If your CSV has 'id', we drop it so SQLite autoincrements.
    """
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        print(f"⚠️ CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    expected_cols = ["id", "title", "priority", "status", "created_date"]
    df = df[expected_cols]

    # drop id to let DB auto-generate
    df = df.drop(columns=["id"])

    df.to_sql("it_tickets", conn, if_exists="append", index=False)

    print(f"✅ Loaded {len(df)} rows into it_tickets")
    return len(df)


# Quick run test
if __name__ == "__main__":
    c = connect_database()
    load_it_tickets_csv(c)
    print(get_all_tickets(c)[:3])
    c.close()