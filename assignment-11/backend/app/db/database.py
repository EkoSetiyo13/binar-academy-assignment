import json
import os
from typing import Dict, List, Any, Optional
from app.core.config import settings
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = settings.DATABASE_FILE
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file exists with proper structure"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({"lists": []}, f)
    
    def read_db(self) -> Dict[str, List[Dict]]:
        """Read the entire database"""
        with open(self.db_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, initialize with empty structure
                return {"lists": []}
    
    def write_db(self, data: Dict[str, List[Dict]]):
        """Write data to the database"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # List operations
    def get_lists(self) -> List[Dict]:
        """Get all lists"""
        data = self.read_db()
        return data.get("lists", [])
    
    def get_list(self, list_id: str) -> Optional[Dict]:
        """Get a specific list by ID"""
        lists = self.get_lists()
        for lst in lists:
            if lst.get("id") == list_id:
                return lst
        return None
    
    def create_list(self, list_data: Dict) -> Dict:
        """Create a new list"""
        data = self.read_db()
        data["lists"].append(list_data)
        self.write_db(data)
        return list_data
    
    def update_list(self, list_id: str, list_data: Dict) -> Optional[Dict]:
        """Update an existing list"""
        data = self.read_db()
        for i, lst in enumerate(data["lists"]):
            if lst.get("id") == list_id:
                # Preserve the tasks
                list_data["tasks"] = lst.get("tasks", [])
                data["lists"][i] = list_data
                self.write_db(data)
                return list_data
        return None
    
    def delete_list(self, list_id: str) -> bool:
        """Delete a list"""
        data = self.read_db()
        initial_count = len(data["lists"])
        data["lists"] = [lst for lst in data["lists"] if lst.get("id") != list_id]
        if len(data["lists"]) < initial_count:
            self.write_db(data)
            return True
        return False
    
    # Task operations
    def get_tasks(self, list_id: str) -> List[Dict]:
        """Get all tasks in a list"""
        lst = self.get_list(list_id)
        if lst:
            return lst.get("tasks", [])
        return []
    
    def get_task(self, list_id: str, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        tasks = self.get_tasks(list_id)
        for task in tasks:
            if task.get("id") == task_id:
                return task
        return None
    
    def add_task(self, list_id: str, task_data: Dict) -> Optional[Dict]:
        """Add a task to a list"""
        data = self.read_db()
        for lst in data["lists"]:
            if lst.get("id") == list_id:
                if "tasks" not in lst:
                    lst["tasks"] = []
                lst["tasks"].append(task_data)
                self.write_db(data)
                return task_data
        return None
    
    def update_task(self, list_id: str, task_id: str, task_data: Dict) -> Optional[Dict]:
        """Update a task"""
        data = self.read_db()
        for lst in data["lists"]:
            if lst.get("id") == list_id:
                for i, task in enumerate(lst.get("tasks", [])):
                    if task.get("id") == task_id:
                        lst["tasks"][i] = task_data
                        self.write_db(data)
                        return task_data
        return None
    
    def delete_task(self, list_id: str, task_id: str) -> bool:
        """Delete a task"""
        data = self.read_db()
        for lst in data["lists"]:
            if lst.get("id") == list_id:
                if "tasks" not in lst:
                    return False
                initial_count = len(lst["tasks"])
                lst["tasks"] = [task for task in lst["tasks"] if task.get("id") != task_id]
                if len(lst["tasks"]) < initial_count:
                    self.write_db(data)
                    return True
        return False
    
    def get_tasks_due_this_week(self) -> List[Dict]:
        """Get all tasks due this week across all lists"""
        data = self.read_db()
        due_this_week = []
        today = datetime.now().date()
        
        for lst in data.get("lists", []):
            for task in lst.get("tasks", []):
                if "deadline" in task:
                    # Parse the deadline string
                    try:
                        deadline_date = datetime.fromisoformat(task["deadline"]).date()
                        days_difference = (deadline_date - today).days
                        
                        # If due within the next 7 days
                        if 0 <= days_difference <= 7:
                            # Add list info to the task
                            task_with_list = task.copy()
                            task_with_list["list_id"] = lst.get("id")
                            task_with_list["list_name"] = lst.get("name")
                            due_this_week.append(task_with_list)
                    except ValueError:
                        # Skip if date format is invalid
                        continue
                        
        return due_this_week
    
    def get_tasks_ordered_by_deadline(self, list_id: str) -> List[Dict]:
        """Get tasks in a list ordered by deadline"""
        tasks = self.get_tasks(list_id)
        
        # Filter tasks with valid deadlines
        tasks_with_deadline = []
        tasks_without_deadline = []
        
        for task in tasks:
            if "deadline" in task:
                try:
                    deadline_date = datetime.fromisoformat(task["deadline"])
                    task_copy = task.copy()
                    task_copy["_parsed_deadline"] = deadline_date
                    tasks_with_deadline.append(task_copy)
                except ValueError:
                    tasks_without_deadline.append(task)
            else:
                tasks_without_deadline.append(task)
        
        # Sort tasks with deadline
        sorted_tasks = sorted(tasks_with_deadline, key=lambda x: x["_parsed_deadline"])
        
        # Remove the temporary parsing field
        for task in sorted_tasks:
            if "_parsed_deadline" in task:
                del task["_parsed_deadline"]
        
        # Return sorted tasks followed by tasks without deadlines
        return sorted_tasks + tasks_without_deadline

# Create a singleton instance
db = Database()
