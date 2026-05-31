# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_name: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
