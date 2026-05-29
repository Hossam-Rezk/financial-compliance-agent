from src.helpers.config import get_settings
import os

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.files_dir = os.path.join(os.getcwd(), "assets", "files")
        
        # create it if it doesn't exist
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)