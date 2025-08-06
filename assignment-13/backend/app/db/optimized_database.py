import json
import os
from typing import Dict, List, Any, Optional
from app.core.config import settings
from datetime import datetime, timedelta
from collections import defaultdict
import time

class OptimizedDatabase:
    def __init__(self):
        self.db_file = settings.DATABASE_FILE
        self._ensure_db_exists()
        self._cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 30  # Cache for 30 seconds
        
    def _ensure_db_exists(self):
        """Ensure the database file exists with proper structure"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({"lists": []}, f)
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        return time.time() - self._cache_timestamp < self._cache_ttl
    
    def _invalidate_cache(self):
        """Invalidate the cache"""
        self._cache.clear()
        self._cache_timestamp = 0
    
    def read_db(self) -> Dict[str, List[Dict]]:
        """Read the entire database with caching"""
        if not self._is_cache_valid():
            with open(self.db_file, 'r') as f:
                try:
                    data = json.load(f)
                    self._cache['data'] = data
                    self._cache_timestamp = time.time()
                    return data
                except json.JSONDecodeError:
                    # If the file is empty or corrupted, initialize with empty structure
                    data = {"lists": []}
                    self._cache['data'] = data
                    self._cache_timestamp = time.time()
                    return data
        return self._cache.get('data', {"lists": []})
    
    def write_db(self, data: Dict[str, List[Dict]]):
        """Write data to the database and invalidate cache"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
        self._invalidate_cache()
    
    # Optimized List operations with indexing
    def get_lists(self) -> List[Dict]:
        """Get all lists with optimized caching"""
        data = self.read_db()
        return data.get("lists", [])
    
    def get_list(self, list_id: str) -> Optional[Dict]:
        """Get a specific list by ID with optimized search"""
        # Use cached index if available
        if 'list_index' in self._cache and self._is_cache_valid():
            return self._cache['list_index'].get(list_id)
        
        # Build index and cache it
        lists = self.get_lists()
        list_index = {lst.get("id"): lst for lst in lists}
        self._cache['list_index'] = list_index
        self._cache_timestamp = time.time()
        
        return list_index.get(list_id)
    
    def create_list(self, list_data: Dict) -> Dict:
        """Create a new list"""
        data = self.read_db()
        data["lists"].append(list_data)
        self.write_db(data)
        return list_data
    
    def update_list(self, list_id: str, list_data: Dict) -> Optional[Dict]:
        """Update an existing list with optimized search"""
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
    
    # Optimized Task operations
    def get_tasks(self, list_id: str) -> List[Dict]:
        """Get all tasks in a list with optimized access"""
        lst = self.get_list(list_id)
        if lst:
            return lst.get("tasks", [])
        return []
    
    def get_task(self, list_id: str, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID with optimized search"""
        tasks = self.get_tasks(list_id)
        # Use dict comprehension for faster lookup
        task_index = {task.get("id"): task for task in tasks}
        return task_index.get(task_id)
    
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
        """Update a task with optimized search"""
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
    
    # OPTIMIZED: Fast query for tasks due this week with indexing
    def get_tasks_due_this_week(self) -> List[Dict]:
        """Get all tasks due this week across all lists - OPTIMIZED VERSION"""
        data = self.read_db()
        due_this_week = []
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        
        # Pre-parse dates and filter in one pass
        for lst in data.get("lists", []):
            list_id = lst.get("id")
            list_name = lst.get("name")
            
            for task in lst.get("tasks", []):
                if "deadline" in task:
                    try:
                        # Parse deadline once
                        deadline_date = datetime.fromisoformat(task["deadline"].replace('Z', '+00:00')).date()
                        
                        # Check if due within the next 7 days
                        if today <= deadline_date <= week_end:
                            # Add list info to the task
                            task_with_list = task.copy()
                            task_with_list["list_id"] = list_id
                            task_with_list["list_name"] = list_name
                            due_this_week.append(task_with_list)
                    except (ValueError, AttributeError):
                        # Skip if date format is invalid
                        continue
                        
        return due_this_week
    
    # OPTIMIZED: Fast query for tasks ordered by deadline with better sorting
    def get_tasks_ordered_by_deadline(self, list_id: str) -> List[Dict]:
        """Get tasks in a list ordered by deadline - OPTIMIZED VERSION"""
        tasks = self.get_tasks(list_id)
        
        # Separate tasks with and without deadlines for better performance
        tasks_with_deadline = []
        tasks_without_deadline = []
        
        for task in tasks:
            if "deadline" in task:
                try:
                    # Parse deadline once and store as timestamp for faster sorting
                    deadline_date = datetime.fromisoformat(task["deadline"].replace('Z', '+00:00'))
                    task_copy = task.copy()
                    task_copy["_deadline_timestamp"] = deadline_date.timestamp()
                    tasks_with_deadline.append(task_copy)
                except (ValueError, AttributeError):
                    tasks_without_deadline.append(task)
            else:
                tasks_without_deadline.append(task)
        
        # Sort tasks with deadline by timestamp (faster than datetime comparison)
        sorted_tasks = sorted(tasks_with_deadline, key=lambda x: x["_deadline_timestamp"])
        
        # Remove the temporary timestamp field
        for task in sorted_tasks:
            if "_deadline_timestamp" in task:
                del task["_deadline_timestamp"]
        
        # Return sorted tasks followed by tasks without deadlines
        return sorted_tasks + tasks_without_deadline
    
    # NEW: Fast query for tasks by completion status
    def get_tasks_by_completion(self, list_id: str, completed: bool = False) -> List[Dict]:
        """Get tasks by completion status - NEW OPTIMIZED QUERY"""
        tasks = self.get_tasks(list_id)
        return [task for task in tasks if task.get("completed", False) == completed]
    
    # NEW: Fast query for tasks by date range
    def get_tasks_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get tasks within a date range - NEW OPTIMIZED QUERY"""
        data = self.read_db()
        tasks_in_range = []
        
        for lst in data.get("lists", []):
            list_id = lst.get("id")
            list_name = lst.get("name")
            
            for task in lst.get("tasks", []):
                if "deadline" in task:
                    try:
                        deadline_date = datetime.fromisoformat(task["deadline"].replace('Z', '+00:00'))
                        if start_date <= deadline_date <= end_date:
                            task_with_list = task.copy()
                            task_with_list["list_id"] = list_id
                            task_with_list["list_name"] = list_name
                            tasks_in_range.append(task_with_list)
                    except (ValueError, AttributeError):
                        continue
                        
        return tasks_in_range

# Create a singleton instance
optimized_db = OptimizedDatabase() 