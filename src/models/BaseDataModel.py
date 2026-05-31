from src.helpers.config import get_settings, Settings

class BaseDataModel:
    def __init__(self, database_client):
        self.db_client = database_client
        self.settings = get_settings()