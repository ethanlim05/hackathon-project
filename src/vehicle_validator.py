import os
import csv
import logging
from utils import validate_plate_format, fuzzy_match, load_csv_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import configuration
try:
    from config import CAR_DATA_PATH, LOG_LEVEL, LOG_FILE
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger.info("Loaded configuration from config.py")
except ImportError:
    # Use defaults if config is not available
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    CAR_DATA_PATH = os.path.join(project_root, 'data', 'car_dataset.csv')
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.warning("config.py not found, using default paths")
    logger.info(f"Using car data path: {CAR_DATA_PATH}")

# Load car data
try:
    car_data = load_csv_data(CAR_DATA_PATH)
    # Convert year_start and year_end to integers
    for car in car_data:
        car['year_start'] = int(car['year_start'])
        car['year_end'] = int(car['year_end'])
    logger.info(f"Car data loaded successfully: {len(car_data)} records")
except Exception as e:
    logger.error(f"Error loading car data: {e}")
    car_data = []

def validate_vehicle(plate: str, brand: str, model: str, year: int):
    logger.info(f"Validating vehicle: plate={plate}, brand={brand}, model={model}, year={year}")
    
    result = {
        "plate": plate,
        "input_brand": brand,
        "input_model": model,
        "input_year": year,
        "suggested_brand": None,
        "suggested_model": None,
        "valid_year_range": None,
        "errors": []
    }

    # --- Plate check ---
    valid_plate, error = validate_plate_format(plate)
    if not valid_plate:
        result["errors"].append(error)

    # --- Brand check ---
    brands = list(set(car['brand'] for car in car_data))
    matched_brand, score = fuzzy_match(brand, brands)
    if matched_brand:
        result["suggested_brand"] = matched_brand
        if matched_brand != brand:
            result["errors"].append("typo_brand")
    else:
        result["errors"].append("invalid_brand")
        return result  # stop early if brand not found

    # --- Model check (for matched brand only) ---
    models = list(set(car['model'] for car in car_data if car['brand'] == matched_brand))
    matched_model, score = fuzzy_match(model, models)
    if matched_model:
        result["suggested_model"] = matched_model
        if matched_model != model:
            result["errors"].append("typo_model")
    else:
        result["errors"].append("invalid_model")
        return result

    # --- Year check ---
    for car in car_data:
        if car['brand'] == matched_brand and car['model'] == matched_model:
            start, end = car['year_start'], car['year_end']
            result["valid_year_range"] = (start, end)
            if year is None:
                result["errors"].append("invalid_year")
            elif not (start <= year <= end):
                result["errors"].append("invalid_year")
            break

    logger.info(f"Validation result: {result['errors'] if result['errors'] else 'No errors'}")
    return result

def main():
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    
    # Load dataset
    try:
        validation_data = load_csv_data(validation_data_path)
        if not validation_data:
            print("No validation data loaded. Exiting.")
            return
        print(f"🔍 Running validation checks on {len(validation_data)} records...\n")
    except Exception as e:
        print(f"Error loading validation data: {e}")
        return

    # Loop through test data
    for index, row in enumerate(validation_data):
        try:
            # Convert year to integer, handle possible conversion errors
            try:
                year = int(row["user_input_year"])
            except ValueError:
                year = None

            result = validate_vehicle(
                plate=row["user_input_plate"],
                brand=row["user_input_brand"],
                model=row["user_input_model"],
                year=year,
            )
            print(f"Row {index}: {result}")
            
            # Print a summary of errors found
            if result["errors"]:
                print(f"  Errors found: {', '.join(result['errors'])}")
            else:
                print("  No errors found - valid entry!")
                
            # Add a separator for better readability
            print("-" * 50)
                
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            print(f"Row data: {row}")

if __name__ == "__main__":
    main()