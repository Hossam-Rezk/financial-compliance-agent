from __future__ import annotations
import os
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from src.models.enums import ResponseStatus
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def ValidateFile(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.file_not_allowed.value
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseStatus.file_too_large.value
        
        return True, ResponseStatus.file_valid.value
    
    def generate_unique_file(self, orig_filename: str, project_id: str):
        random_key = self.generate_random_string()
        project_dir = ProjectController().get_project_dir(project_id=project_id)
        cleaned_filename = self.clean_file_name(filename= orig_filename)
        new_file_path = os.path.join(project_dir, random_key + "_" + cleaned_filename)
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_dir, random_key + "_" + cleaned_filename)
        return new_file_path
    
    def clean_file_name(self, filename: str):
        # Remove any special characters and spaces from the filename
        cleaned_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
        return cleaned_filename