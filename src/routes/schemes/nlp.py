from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The search query")
    top_k: Optional[int] = Field(default=5, ge=1, le=20)
