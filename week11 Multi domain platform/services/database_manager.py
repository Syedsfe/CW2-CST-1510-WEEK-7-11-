import sqlite3
from typing import Iterable, Any

class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection: sqlite3.Connection | None = None

    def connect(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)

    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()

    def execute_query(self, sql: str, params: Iterable[Any] = ()):
        self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur
