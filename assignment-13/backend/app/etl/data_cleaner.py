import json
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, data_file: str, users_file: str):
        self.data_file = data_file
        self.users_file = users_file
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self) -> str:
        """Create backup of current data files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        # Backup data.json
        if os.path.exists(self.data_file):
            import shutil
            shutil.copy2(self.data_file, backup_path / "data.json")
            logger.info(f"Backed up data.json to {backup_path / 'data.json'}")
        
        # Backup users.json
        if os.path.exists(self.users_file):
            import shutil
            shutil.copy2(self.users_file, backup_path / "users.json")
            logger.info(f"Backed up users.json to {backup_path / 'users.json'}")
        
        return str(backup_path)
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON files"""
        data = {}
        
        # Load main data
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data['lists'] = json.load(f)
        else:
            data['lists'] = []
            logger.warning(f"Data file {self.data_file} not found, creating empty structure")
        
        # Load users
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                data['users'] = json.load(f)
        else:
            data['users'] = {}
            logger.warning(f"Users file {self.users_file} not found, creating empty structure")
        
        return data
    
    def save_data(self, data: Dict[str, Any]):
        """Save cleaned data back to files"""
        # Save lists data
        with open(self.data_file, 'w') as f:
            json.dump(data['lists'], f, indent=2)
        logger.info(f"Saved cleaned data to {self.data_file}")
        
        # Save users data
        with open(self.users_file, 'w') as f:
            json.dump(data['users'], f, indent=2)
        logger.info(f"Saved cleaned users to {self.users_file}")
    
    def clean_lists_data(self, lists: List[Dict]) -> List[Dict]:
        """Clean lists data - remove duplicates, fix invalid data"""
        cleaned_lists = []
        seen_ids = set()
        seen_names = set()
        
        for list_item in lists:
            # Skip if no ID
            if not list_item.get('id'):
                logger.warning(f"Skipping list without ID: {list_item}")
                continue
            
            # Skip duplicates by ID
            if list_item['id'] in seen_ids:
                logger.warning(f"Skipping duplicate list ID: {list_item['id']}")
                continue
            seen_ids.add(list_item['id'])
            
            # Clean list data
            cleaned_list = {
                'id': list_item['id'],
                'name': self._clean_string(list_item.get('name', '')),
                'description': self._clean_string(list_item.get('description', '')),
                'tasks': self._clean_tasks_data(list_item.get('tasks', []))
            }
            
            # Skip lists with empty names (unless it's the only list)
            if not cleaned_list['name'].strip() and len(lists) > 1:
                logger.warning(f"Skipping list with empty name: {list_item['id']}")
                continue
            
            # Skip duplicate names (unless it's the only list)
            if cleaned_list['name'].strip() in seen_names and len(lists) > 1:
                logger.warning(f"Skipping list with duplicate name: {cleaned_list['name']}")
                continue
            seen_names.add(cleaned_list['name'].strip())
            
            cleaned_lists.append(cleaned_list)
        
        return cleaned_lists
    
    def clean_tasks_data(self, tasks: List[Dict]) -> List[Dict]:
        """Clean tasks data - remove duplicates, fix invalid data"""
        cleaned_tasks = []
        seen_task_ids = set()
        
        for task in tasks:
            # Skip if no ID
            if not task.get('id'):
                logger.warning(f"Skipping task without ID: {task}")
                continue
            
            # Skip duplicates by ID
            if task['id'] in seen_task_ids:
                logger.warning(f"Skipping duplicate task ID: {task['id']}")
                continue
            seen_task_ids.add(task['id'])
            
            # Clean task data
            cleaned_task = {
                'id': task['id'],
                'title': self._clean_string(task.get('title', '')),
                'description': self._clean_string(task.get('description', '')),
                'completed': bool(task.get('completed', False)),
                'created_at': self._clean_datetime(task.get('created_at')),
                'deadline': self._clean_datetime(task.get('deadline'))
            }
            
            # Skip tasks with empty titles
            if not cleaned_task['title'].strip():
                logger.warning(f"Skipping task with empty title: {task['id']}")
                continue
            
            cleaned_tasks.append(cleaned_task)
        
        return cleaned_tasks
    
    def clean_users_data(self, users: Dict[str, Any]) -> Dict[str, Any]:
        """Clean users data - remove invalid entries, fix data types"""
        cleaned_users = {}
        
        for user_id, user_data in users.items():
            # Skip if no user data
            if not user_data:
                logger.warning(f"Skipping empty user data for ID: {user_id}")
                continue
            
            # Clean user data
            cleaned_user = {
                'id': user_id,
                'username': self._clean_string(user_data.get('username', '')),
                'email': self._clean_email(user_data.get('email', '')),
                'hashed_password': user_data.get('hashed_password', ''),
                'created_at': self._clean_datetime(user_data.get('created_at'))
            }
            
            # Skip users with empty username or email
            if not cleaned_user['username'].strip():
                logger.warning(f"Skipping user with empty username: {user_id}")
                continue
            
            if not cleaned_user['email'].strip():
                logger.warning(f"Skipping user with empty email: {user_id}")
                continue
            
            # Validate email format
            if not self._is_valid_email(cleaned_user['email']):
                logger.warning(f"Skipping user with invalid email: {cleaned_user['email']}")
                continue
            
            cleaned_users[user_id] = cleaned_user
        
        return cleaned_users
    
    def _clean_string(self, value: Any) -> str:
        """Clean string values - remove null, convert to string, trim whitespace"""
        if value is None:
            return ""
        return str(value).strip()
    
    def _clean_datetime(self, value: Any) -> Optional[str]:
        """Clean datetime values - validate and standardize format"""
        if value is None:
            return None
        
        try:
            # Try to parse and standardize datetime
            if isinstance(value, str):
                # Handle various datetime formats
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.isoformat()
            elif isinstance(value, datetime):
                return value.isoformat()
            else:
                return None
        except (ValueError, TypeError):
            logger.warning(f"Invalid datetime format: {value}")
            return None
    
    def _clean_email(self, email: str) -> str:
        """Clean email - lowercase and trim"""
        if not email:
            return ""
        return email.lower().strip()
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using regex"""
        if not email:
            return False
        
        # Simple email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    def generate_cleaning_report(self, original_data: Dict, cleaned_data: Dict) -> Dict[str, Any]:
        """Generate a report of cleaning operations"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'backup_created': True,
            'lists_cleaned': {
                'original_count': len(original_data.get('lists', [])),
                'cleaned_count': len(cleaned_data.get('lists', [])),
                'removed_count': len(original_data.get('lists', [])) - len(cleaned_data.get('lists', []))
            },
            'users_cleaned': {
                'original_count': len(original_data.get('users', {})),
                'cleaned_count': len(cleaned_data.get('users', {})),
                'removed_count': len(original_data.get('users', {})) - len(cleaned_data.get('users', {}))
            },
            'tasks_cleaned': {
                'original_count': sum(len(list_item.get('tasks', [])) for list_item in original_data.get('lists', [])),
                'cleaned_count': sum(len(list_item.get('tasks', [])) for list_item in cleaned_data.get('lists', []))
            }
        }
        
        return report
    
    def run_cleaning_pipeline(self) -> Dict[str, Any]:
        """Run the complete data cleaning pipeline"""
        logger.info("Starting data cleaning pipeline...")
        
        # Create backup
        backup_path = self.create_backup()
        logger.info(f"Backup created at: {backup_path}")
        
        # Load original data
        original_data = self.load_data()
        logger.info("Loaded original data")
        
        # Clean data
        cleaned_data = {
            'lists': self.clean_lists_data(original_data.get('lists', [])),
            'users': self.clean_users_data(original_data.get('users', {}))
        }
        
        # Save cleaned data
        self.save_data(cleaned_data)
        
        # Generate report
        report = self.generate_cleaning_report(original_data, cleaned_data)
        report['backup_path'] = backup_path
        
        logger.info("Data cleaning pipeline completed successfully")
        return report

def main():
    """Main function to run the ETL pipeline"""
    # Initialize cleaner with file paths
    data_file = "app/db/data.json"
    users_file = "app/db/users.json"
    
    cleaner = DataCleaner(data_file, users_file)
    
    try:
        # Run cleaning pipeline
        report = cleaner.run_cleaning_pipeline()
        
        # Print report
        print("\n" + "="*50)
        print("DATA CLEANING REPORT")
        print("="*50)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Backup created: {report['backup_path']}")
        print(f"\nLists cleaned:")
        print(f"  Original: {report['lists_cleaned']['original_count']}")
        print(f"  Cleaned: {report['lists_cleaned']['cleaned_count']}")
        print(f"  Removed: {report['lists_cleaned']['removed_count']}")
        print(f"\nUsers cleaned:")
        print(f"  Original: {report['users_cleaned']['original_count']}")
        print(f"  Cleaned: {report['users_cleaned']['cleaned_count']}")
        print(f"  Removed: {report['users_cleaned']['removed_count']}")
        print(f"\nTasks cleaned:")
        print(f"  Original: {report['tasks_cleaned']['original_count']}")
        print(f"  Cleaned: {report['tasks_cleaned']['cleaned_count']}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise

if __name__ == "__main__":
    main() 