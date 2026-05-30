from src.helpers.config import get_settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.files_dir = os.path.join(os.getcwd(), "assets", "files")
        
        # create it if it doesn't exist
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
    def generate_random_string(self, length=8):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))