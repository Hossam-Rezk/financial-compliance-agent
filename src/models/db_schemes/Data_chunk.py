from pydantic import BaseModel, Field,validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., description="Text content of the chunk", min_length=1)
    chunk_metadata: dict = Field(..., description="Metadata associated with the chunk")
    chunk_order: int = Field(..., description="Order of the chunk in the original document", gt=0)
    chunk_project_id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True