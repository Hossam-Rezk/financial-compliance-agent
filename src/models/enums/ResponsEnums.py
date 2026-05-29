from enum import Enum
class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    file_not_allowed = "file_not_allowed"
    file_too_large = "file_too_large"
    file_valid = "file_valid"
    