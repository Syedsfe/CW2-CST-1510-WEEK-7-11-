class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self, incident_id: int, title: str, severity: str, status: str, date: str):
        self.__id = incident_id
        self.__title = title
        self.__severity = severity.lower()
        self.__status = status
        self.__date = date

    def get_id(self) -> int:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_date(self) -> str:
        return self.__date

    def update_status(self, new_status: str):
        self.__status = new_status

    def update_title(self, new_title: str):
        self.__title = new_title

    def update_severity(self, new_severity: str):
        self.__severity = new_severity.lower()

    def get_severity_level(self) -> int:
        """Return an integer severity level based on guide mapping."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return mapping.get(self.__severity, 0)

    def __str__(self):
        return f"Incident {self.__id} [{self.__severity.upper()}] – {self.__title}"
