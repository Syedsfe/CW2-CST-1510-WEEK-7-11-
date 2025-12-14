import bcrypt

class BcryptHasher:
    """Handles password hashing using bcrypt."""

    @staticmethod
    def hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager

class AuthManager:
    """Handles user registration and login using SQLite."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str, role="user") -> bool:
        """Register a new user. Returns True if successful, False if username exists."""
        
        # Check if username already exists
        row = self._db.fetch_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        if row:
            return False  # Username taken

        password_hash = BcryptHasher.hash_password(password)

        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        return True

    def login_user(self, username: str, password: str) -> Optional[User]:
        """Return User object if login successful, else None."""

        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if not row:
            return None

        username_db, hash_db, role_db = row

        if BcryptHasher.check_password(password, hash_db):
            return User(username_db, hash_db, role_db)

        return None
