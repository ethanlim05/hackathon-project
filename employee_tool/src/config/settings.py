# src/config/settings.py
import os

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Data directory
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# File paths
EMPLOYEE_CREDENTIALS_PATH = os.path.join(DATA_DIR, 'employee_credentials.csv')
CUSTOMER_DATA_PATH = os.path.join(DATA_DIR, 'customer_data.csv')
VEHICLE_GRANTS_PATH = os.path.join(DATA_DIR, 'vehicle_grants.csv')
VALIDATION_RESULTS_PATH = os.path.join(DATA_DIR, 'validation_results.csv')

# Try multiple possible paths for car_dataset.csv
possible_car_paths = [
    os.path.join(PROJECT_ROOT, '..', 'data', 'car_dataset.csv'),  # If employee_tool is at same level as hackathon-project
    os.path.join(PROJECT_ROOT, '..', 'hackathon-project', 'data', 'car_dataset.csv'),  # If employee_tool is inside hackathon-project
    os.path.join(DATA_DIR, 'car_dataset.csv')  # If car_dataset is in employee_tool data folder
]

# Use the first path that exists
CAR_DATA_PATH = None
for path in possible_car_paths:
    if os.path.exists(path):
        CAR_DATA_PATH = path
        break

# If none found, use the first option as default
if CAR_DATA_PATH is None:
    CAR_DATA_PATH = possible_car_paths[0]

# Validation thresholds
FUZZY_MATCH_THRESHOLD = 80
MAX_LEVENSHTEIN_DISTANCE = 3

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(PROJECT_ROOT, 'employee_tool.log')