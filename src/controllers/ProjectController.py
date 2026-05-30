from .BaseController import BaseController
from fastapi import UploadFile
from src.models.enums import ResponseStatus
from src.helpers.config import get_settings
import os
from os import path

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_dir(self, project_id: str):
        project_dir = os.path.join(self.files_dir, project_id)
    
        if not path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
    
