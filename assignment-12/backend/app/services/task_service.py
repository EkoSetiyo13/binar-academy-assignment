from app.db.database import db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskInDB, TaskResponse
from typing import List, Optional, Dict
from datetime import datetime

class TaskService:
    @staticmethod
    def get_tasks(list_id: str) -> List[Dict]:
        """Get all tasks in a list"""
        return db.get_tasks(list_id)
    
    @staticmethod
    def get_task(list_id: str, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        return db.get_task(list_id, task_id)
    
    @staticmethod
    def add_task(list_id: str, task_data: TaskCreate) -> Optional[Dict]:
        """Add a task to a list"""
        # Convert to DB model with ID and timestamps
        task_in_db = TaskInDB(**task_data.model_dump())
        
        # Format datetime to ISO string for JSON storage
        task_dict = task_in_db.model_dump()
        if task_dict.get("deadline"):
            task_dict["deadline"] = task_dict["deadline"].isoformat()
        task_dict["created_at"] = task_dict["created_at"].isoformat()
        
        # Add to database
        added_task = db.add_task(list_id, task_dict)
        return added_task
    
    @staticmethod
    def update_task(list_id: str, task_id: str, task_data: TaskUpdate) -> Optional[Dict]:
        """Update a task"""
        # Get current task
        existing_task = db.get_task(list_id, task_id)
        if not existing_task:
            return None
        
        # Update only provided fields
        for key, value in task_data.model_dump(exclude_unset=True).items():
            if value is not None:
                # Format datetime to ISO string for JSON storage
                if key == "deadline" and value:
                    existing_task[key] = value.isoformat()
                else:
                    existing_task[key] = value
        
        # Update in database
        updated_task = db.update_task(list_id, task_id, existing_task)
        return updated_task
    
    @staticmethod
    def delete_task(list_id: str, task_id: str) -> bool:
        """Delete a task"""
        return db.delete_task(list_id, task_id)
    
    @staticmethod
    def toggle_task_completion(list_id: str, task_id: str) -> Optional[Dict]:
        """Toggle a task's completion status"""
        # Get current task
        existing_task = db.get_task(list_id, task_id)
        if not existing_task:
            return None
        
        # Toggle completion
        existing_task["completed"] = not existing_task.get("completed", False)
        
        # Update in database
        updated_task = db.update_task(list_id, task_id, existing_task)
        return updated_task
    
    @staticmethod
    def get_tasks_due_this_week() -> List[Dict]:
        """Get all tasks due this week across all lists"""
        return db.get_tasks_due_this_week()
    
    @staticmethod
    def get_tasks_ordered_by_deadline(list_id: str) -> List[Dict]:
        """Get tasks in a list ordered by deadline"""
        return db.get_tasks_ordered_by_deadline(list_id)
