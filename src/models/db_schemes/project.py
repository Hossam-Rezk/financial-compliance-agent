from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., description="Unique identifier for the project", min_length=1)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True