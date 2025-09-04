import os

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Data directory
DATA_DIR = os.path.join(PROJECT_ROOT, '..', 'data')

# File paths
CAR_DATA_PATH = os.path.join(DATA_DIR, 'car_dataset.csv')
VALIDATION_DATA_PATH = os.path.join(DATA_DIR, 'validation_dataset.csv')

# Validation thresholds
FUZZY_MATCH_THRESHOLD = 80
MAX_LEVENSHTEIN_DISTANCE = 3

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(PROJECT_ROOT, 'validation.log')