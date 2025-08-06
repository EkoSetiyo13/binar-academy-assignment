# This file contains intentional code smells to demonstrate SonarCloud quality gate failure
# This should be removed after testing

import os
import sys
from typing import Dict, List, Any

# Code Smell 1: Unused imports
import json
import xml.etree.ElementTree as ET  # This import is never used

# Code Smell 2: Hardcoded credentials (security issue)
DATABASE_PASSWORD = "admin123"  # This is a security vulnerability
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key

# Code Smell 3: Magic numbers
def calculate_discount(price: float) -> float:
    return price * 0.15  # Magic number 0.15 should be a constant

# Code Smell 4: Long function with too many responsibilities
def process_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    This function does too many things - violates Single Responsibility Principle
    """
    # Validate user data
    if not user_data.get('name'):
        raise ValueError("Name is required")
    if not user_data.get('email'):
        raise ValueError("Email is required")
    if not user_data.get('age'):
        raise ValueError("Age is required")
    
    # Process user data
    processed_data = {}
    processed_data['name'] = user_data['name'].upper()
    processed_data['email'] = user_data['email'].lower()
    processed_data['age'] = int(user_data['age'])
    
    # Calculate user category
    if processed_data['age'] < 18:
        processed_data['category'] = 'minor'
    elif processed_data['age'] < 65:
        processed_data['category'] = 'adult'
    else:
        processed_data['category'] = 'senior'
    
    # Add timestamp
    import datetime
    processed_data['processed_at'] = datetime.datetime.now().isoformat()
    
    # Log the processing
    print(f"Processed user: {processed_data['name']}")
    
    # Save to database (simulated)
    save_to_database(processed_data)
    
    # Send notification (simulated)
    send_notification(processed_data)
    
    return processed_data

# Code Smell 5: Empty function
def empty_function():
    pass

# Code Smell 6: Duplicate code
def validate_email(email: str) -> bool:
    if '@' in email and '.' in email:
        return True
    return False

def validate_email_duplicate(email: str) -> bool:  # Duplicate of above function
    if '@' in email and '.' in email:
        return True
    return False

# Code Smell 7: Dead code
def unused_function():
    return "This function is never called"

# Code Smell 8: Inconsistent naming
def getUserData():  # Should be snake_case
    return {"name": "John", "age": 30}

def process_user_data_2(user_data):  # Missing type hints
    return user_data

# Code Smell 9: Complex conditional
def determine_user_status(user):
    if user.get('age') and user.get('age') > 0 and user.get('age') < 150 and user.get('name') and len(user.get('name', '')) > 0 and user.get('email') and '@' in user.get('email', '') and '.' in user.get('email', ''):
        return "valid"
    else:
        return "invalid"

# Code Smell 10: Exception handling without specific exception
def risky_operation():
    try:
        result = 10 / 0
        return result
    except:  # Should catch specific exceptions
        return None

# Code Smell 11: Global variable
global_counter = 0

def increment_counter():
    global global_counter
    global_counter += 1
    return global_counter

# Code Smell 12: Long parameter list
def create_user(name, email, age, phone, address, city, state, zip_code, country, preferences, settings, metadata):
    # Too many parameters - should use a data class or dictionary
    return {
        'name': name,
        'email': email,
        'age': age,
        'phone': phone,
        'address': address,
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'country': country,
        'preferences': preferences,
        'settings': settings,
        'metadata': metadata
    }

# Helper functions (these are fine)
def save_to_database(data: Dict[str, Any]) -> None:
    # Simulated database save
    pass

def send_notification(data: Dict[str, Any]) -> None:
    # Simulated notification
    pass 