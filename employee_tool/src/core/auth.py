# src/core/auth.py
import os
import csv
import hashlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_employee(employee_id, password):
    """
    Verify employee credentials.
    
    Args:
        employee_id (str): Employee ID
        password (str): Password
        
    Returns:
        tuple: (is_valid, employee_data)
    """
    from config.settings import EMPLOYEE_CREDENTIALS_PATH
    
    if not os.path.exists(EMPLOYEE_CREDENTIALS_PATH):
        logger.error(f"Employee credentials file not found: {EMPLOYEE_CREDENTIALS_PATH}")
        return False, None
    
    hashed_password = hash_password(password)
    
    try:
        with open(EMPLOYEE_CREDENTIALS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['employee_id'] == employee_id and row['password_hash'] == hashed_password:
                    if row.get('active', 'True').lower() == 'true':
                        # Log successful login
                        logger.info(f"Employee {employee_id} logged in successfully at {datetime.now()}")
                        return True, row
                    else:
                        logger.warning(f"Inactive employee {employee_id} attempted login at {datetime.now()}")
                        return False, None
        
        logger.warning(f"Failed login attempt for employee {employee_id} at {datetime.now()}")
        return False, None
    except Exception as e:
        logger.error(f"Error verifying employee credentials: {e}")
        return False, None

def add_employee(employee_id, name, password, role='validator'):
    """
    Add a new employee to the credentials file.
    
    Args:
        employee_id (str): Employee ID
        name (str): Employee name
        password (str): Password
        role (str): Employee role
        
    Returns:
        bool: Success status
    """
    from config.settings import EMPLOYEE_CREDENTIALS_PATH
    
    # Check if employee already exists
    if os.path.exists(EMPLOYEE_CREDENTIALS_PATH):
        try:
            with open(EMPLOYEE_CREDENTIALS_PATH, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['employee_id'] == employee_id:
                        logger.warning(f"Employee {employee_id} already exists")
                        return False
        except Exception as e:
            logger.error(f"Error checking existing employees: {e}")
            return False
    
    # Create file if it doesn't exist
    if not os.path.exists(EMPLOYEE_CREDENTIALS_PATH):
        os.makedirs(os.path.dirname(EMPLOYEE_CREDENTIALS_PATH), exist_ok=True)
        with open(EMPLOYEE_CREDENTIALS_PATH, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['employee_id', 'name', 'password_hash', 'role', 'active', 'created_at'])
            writer.writeheader()
    
    # Add new employee
    try:
        with open(EMPLOYEE_CREDENTIALS_PATH, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['employee_id', 'name', 'password_hash', 'role', 'active', 'created_at'])
            writer.writerow({
                'employee_id': employee_id,
                'name': name,
                'password_hash': hash_password(password),
                'role': role,
                'active': 'True',
                'created_at': datetime.now().isoformat()
            })
        
        logger.info(f"New employee {employee_id} added successfully")
        return True
    except Exception as e:
        logger.error(f"Error adding new employee: {e}")
        return False