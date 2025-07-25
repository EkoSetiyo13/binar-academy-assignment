from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class ListBase(BaseModel):
    name: str
    description: Optional[str] = None

class ListCreate(ListBase):
    pass

class ListUpdate(ListBase):
    name: Optional[str] = None

class ListInDB(ListBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class ListResponse(ListInDB):
    tasks: List = []
