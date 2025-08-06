# This file contains clean code after fixing all code smells
# This demonstrates quality gate success

import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

# Constants instead of magic numbers
DISCOUNT_RATE = 0.15
MINOR_AGE = 18
SENIOR_AGE = 65
MAX_AGE = 150

# Use environment variables for sensitive data
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
API_KEY = os.getenv("API_KEY", "")

@dataclass
class UserData:
    """Data class for user information"""
    name: str
    email: str
    age: int
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class UserValidator:
    """Class responsible for user data validation"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        return '@' in email and '.' in email
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """Validate age range"""
        return 0 < age < MAX_AGE
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate name is not empty"""
        return bool(name and name.strip())

class UserProcessor:
    """Class responsible for user data processing"""
    
    @staticmethod
    def process_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user data with single responsibility"""
        # Validate user data
        if not UserValidator.validate_name(user_data.get('name', '')):
            raise ValueError("Name is required")
        if not UserValidator.validate_email(user_data.get('email', '')):
            raise ValueError("Email is required")
        if not UserValidator.validate_age(user_data.get('age', 0)):
            raise ValueError("Valid age is required")
        
        # Process user data
        processed_data = {
            'name': user_data['name'].upper(),
            'email': user_data['email'].lower(),
            'age': int(user_data['age']),
            'category': UserProcessor._calculate_category(int(user_data['age'])),
            'processed_at': datetime.now().isoformat()
        }
        
        return processed_data
    
    @staticmethod
    def _calculate_category(age: int) -> str:
        """Calculate user category based on age"""
        if age < MINOR_AGE:
            return 'minor'
        elif age < SENIOR_AGE:
            return 'adult'
        else:
            return 'senior'

class DiscountCalculator:
    """Class responsible for discount calculations"""
    
    @staticmethod
    def calculate_discount(price: float) -> float:
        """Calculate discount with constant rate"""
        return price * DISCOUNT_RATE

class UserStatusDeterminer:
    """Class responsible for determining user status"""
    
    @staticmethod
    def determine_user_status(user: Dict[str, Any]) -> str:
        """Determine user status with simplified logic"""
        has_valid_age = UserValidator.validate_age(user.get('age', 0))
        has_valid_name = UserValidator.validate_name(user.get('name', ''))
        has_valid_email = UserValidator.validate_email(user.get('email', ''))
        
        if has_valid_age and has_valid_name and has_valid_email:
            return "valid"
        return "invalid"

class SafeOperationHandler:
    """Class responsible for safe operations"""
    
    @staticmethod
    def safe_division(numerator: float, denominator: float) -> Optional[float]:
        """Safe division with specific exception handling"""
        try:
            if denominator == 0:
                raise ValueError("Division by zero")
            return numerator / denominator
        except (ValueError, ZeroDivisionError) as e:
            print(f"Division error: {e}")
            return None

class UserCreator:
    """Class responsible for user creation"""
    
    @staticmethod
    def create_user(user_data: UserData) -> Dict[str, Any]:
        """Create user with data class"""
        return {
            'name': user_data.name,
            'email': user_data.email,
            'age': user_data.age,
            'phone': user_data.phone,
            'address': user_data.address,
            'city': user_data.city,
            'state': user_data.state,
            'zip_code': user_data.zip_code,
            'country': user_data.country,
            'preferences': user_data.preferences,
            'settings': user_data.settings,
            'metadata': user_data.metadata
        }

class DatabaseManager:
    """Class responsible for database operations"""
    
    @staticmethod
    def save_to_database(data: Dict[str, Any]) -> None:
        """Save data to database"""
        # Simulated database save
        print(f"Saving to database: {data}")
    
    @staticmethod
    def send_notification(data: Dict[str, Any]) -> None:
        """Send notification"""
        # Simulated notification
        print(f"Sending notification: {data}")

# Example usage
def main():
    """Main function demonstrating clean code usage"""
    # Create user data
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    
    # Process user data
    try:
        processed_user = UserProcessor.process_user_data(user_data)
        print(f"Processed user: {processed_user}")
        
        # Calculate discount
        discount = DiscountCalculator.calculate_discount(100.0)
        print(f"Discount: {discount}")
        
        # Determine status
        status = UserStatusDeterminer.determine_user_status(user_data)
        print(f"User status: {status}")
        
        # Safe operation
        result = SafeOperationHandler.safe_division(10, 2)
        print(f"Safe division result: {result}")
        
        # Create user with data class
        user = UserData(
            name="Jane Doe",
            email="jane@example.com",
            age=25
        )
        created_user = UserCreator.create_user(user)
        print(f"Created user: {created_user}")
        
    except ValueError as e:
        print(f"Validation error: {e}")

if __name__ == "__main__":
    main() 