class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""

    def __init__(self, username: str, password_hash: str, role: str = "user"):
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    def get_username(self) -> str:
        return self.__username

    def get_role(self) -> str:
        return self.__role

    def verify_password(self, plain_password: str, hasher) -> bool:
        """Check if the provided password matches the stored hash."""
        return hasher.check_password(plain_password, self.__password_hash)

    def __str__(self):
        return f"User({self.__username}, role={self.__role})"
