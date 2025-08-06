from app.db.database import db
from app.schemas.list_schema import ListCreate, ListUpdate, ListInDB, ListResponse
from typing import List, Optional, Dict

class ListService:
    @staticmethod
    def get_lists() -> List[Dict]:
        """Get all lists with their tasks"""
        return db.get_lists()
    
    @staticmethod
    def get_list(list_id: str) -> Optional[Dict]:
        """Get a specific list by ID"""
        return db.get_list(list_id)
    
    @staticmethod
    def create_list(list_data: ListCreate) -> Dict:
        """Create a new list"""
        # Convert to DB model with ID
        list_in_db = ListInDB(**list_data.model_dump())
        
        # Create in database
        created_list = db.create_list(list_in_db.model_dump())
        return created_list
    
    @staticmethod
    def update_list(list_id: str, list_data: ListUpdate) -> Optional[Dict]:
        """Update an existing list"""
        # Get current list
        existing_list = db.get_list(list_id)
        if not existing_list:
            return None
        
        # Update only provided fields
        for key, value in list_data.model_dump(exclude_unset=True).items():
            if value is not None:
                existing_list[key] = value
        
        # Update in database
        updated_list = db.update_list(list_id, existing_list)
        return updated_list
    
    @staticmethod
    def delete_list(list_id: str) -> bool:
        """Delete a list"""
        return db.delete_list(list_id)
