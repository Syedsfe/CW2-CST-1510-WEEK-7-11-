class Dataset:
    """Represents a dataset entry in the Data Science module."""

    def __init__(self, dataset_id: int, name: str, category: str, source: str,
                 last_updated: str, record_count: int, file_size_mb: float):
        self.__id = dataset_id
        self.__name = name
        self.__category = category
        self.__source = source
        self.__last_updated = last_updated
        self.__record_count = record_count
        self.__file_size_mb = file_size_mb

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_source(self):
        return self.__source

    def get_last_updated(self):
        return self.__last_updated

    def get_row_count(self):
        return self.__record_count

    def get_size_mb(self):
        return self.__file_size_mb

    def __str__(self):
        return f"Dataset({self.__id}): {self.__name} [{self.__category}] – {self.__file_size_mb} MB"
