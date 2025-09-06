import os
import sys
import csv
import logging

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

logger = logging.getLogger(__name__)

def load_csv_data(file_path):
    """
    Load CSV data without pandas.
    Returns a list of dictionaries.
    """
    data = []
    
    # Convert to absolute path if it's a relative path
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)
    
    logger.info(f"Loading data from: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return data
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        logger.info(f"Successfully loaded {len(data)} rows from {file_path}")
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
    
    return data

def load_car_data(car_data_path):
    """Load car data from CSV."""
    car_data = load_csv_data(car_data_path)
    # Convert year_start and year_end to integers
    for car in car_data:
        car['year_start'] = int(car['year_start'])
        car['year_end'] = int(car['year_end'])
    return car_data

if __name__ == "__main__":
    # Test the functions
    print("Testing data_loader functions:")
    
    # Test load_csv_data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'data')
    car_data_path = os.path.join(data_dir, 'car_dataset.csv')
    
    csv_data = load_csv_data(car_data_path)
    print(f"Loaded {len(csv_data)} rows from CSV")
    
    # Test load_car_data
    car_data = load_car_data(car_data_path)
    print(f"Loaded car data with {len(car_data)} records")
    if car_data:
        print(f"First record: {car_data[0]}")