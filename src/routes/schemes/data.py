from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    project_id: str
    file_name: str
    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0

    