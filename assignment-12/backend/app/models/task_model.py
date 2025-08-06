from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskModel(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    deadline: Optional[datetime] = None
    created_at: datetime
