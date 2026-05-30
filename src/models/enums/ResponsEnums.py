from enum import Enum
class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    file_not_allowed = "file_not_allowed"
    file_too_large = "file_too_large"
    file_valid = "file_valid"
    processing_failed = "processing_failed"
    processing_successful = "processing_successful"