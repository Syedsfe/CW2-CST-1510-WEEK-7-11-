import sqlite3
from sqlite3 import Error

class DatabaseManager:

    def __init__(self, db_path="intelligence_platform.db"):
        """
        Initialize the connection to the SQLite database.
        """
        self.db_path = db_path
        self.conn = None
        self.connect_to_database()

    def connect_to_database(self):
        """
        Create a database connection.
        """
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        except Error as e:
            print("Database connection error:", e)

    def create_user(self, username, password, role="user"):
        """
        Insert a new user into the users table.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            return True
        except Error as e:
            print("Error creating user:", e)
            return False

    def verify_user(self, username, password):
        """
        Validate a user's login credentials.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT role FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            result = cursor.fetchone()
            return result  # returns role if match found
        except Error as e:
            print("User verification error:", e)
            return None

    def fetch_all(self, query, params=()):
        """
        Run a SELECT query and return all results.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def execute_query(self, query, params=()):
        """
        Run INSERT, UPDATE, DELETE queries.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return True
        except Error as e:
            print("Query execution error:", e)
            return False

    def __del__(self):
        """
        Close connection when object is destroyed.
        """
        if self.conn:
            self.conn.close()