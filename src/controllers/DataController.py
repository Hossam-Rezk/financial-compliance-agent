from __future__ import annotations
from .BaseController import BaseController
from fastapi import UploadFile
from src.models.enums import ResponseStatus
class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def ValidateFile(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.file_not_allowed.value
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseStatus.file_too_large.value
        
        return True, ResponseStatus.file_valid.value