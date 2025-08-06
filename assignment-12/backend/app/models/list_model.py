from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ListModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tasks: List[Dict[str, Any]] = []
