import re
import csv
import os
import traceback

def validate_plate_format(plate: str):
    """
    Validate Malaysian plate format:
    - 1–3 letters
    - optional space
    - 1–4 digits
    - optional trailing letter
    """
    pattern = r"^[A-Z]{1,3}\s?[0-9]{1,4}[A-Z]?$"
    if not re.match(pattern, plate.upper()):
        return False, "plate_format_error"
    return True, None

def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    This is used for fuzzy matching without external libraries.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def fuzzy_match(query: str, choices: list, threshold: int = 80):
    """
    Match user input to closest valid choice using Levenshtein distance.
    Returns (best_match, score).
    """
    if not choices:
        return None, 0
    
    best_match = None
    best_score = 0
    
    # Try normal matching first
    for choice in choices:
        distance = levenshtein_distance(query.lower(), choice.lower())
        max_len = max(len(query), len(choice))
        similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
        
        if similarity >= threshold and similarity > best_score:
            best_match = choice
            best_score = similarity
    
    # If no good match found, try reversed string (for cases like "notorP" -> "Proton")
    if best_match is None:
        reversed_query = query[::-1]  # Reverse the string
        for choice in choices:
            distance = levenshtein_distance(reversed_query.lower(), choice.lower())
            max_len = max(len(reversed_query), len(choice))
            similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
            
            if similarity >= threshold and similarity > best_score:
                best_match = choice
                best_score = similarity
    
    return best_match, best_score

def load_csv_data(file_path):
    """
    Load CSV data without pandas.
    Returns a list of dictionaries.
    """
    data = []
    print(f"Loading data from: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return data
    
    # Check file size
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size} bytes")
    
    if file_size == 0:
        print("Error: File is empty")
        return data
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Print first few lines for debugging
            print("First 5 lines of the file:")
            for i, line in enumerate(file):
                if i < 5:
                    print(f"Line {i+1}: {line.strip()}")
                else:
                    break
            
            # Reset file pointer to beginning
            file.seek(0)
            
            # Read CSV
            reader = csv.DictReader(file)
            print(f"CSV headers: {reader.fieldnames}")
            
            for row in reader:
                data.append(row)
                # Print first row for debugging
                if len(data) == 1:
                    print(f"First data row: {row}")
            
        print(f"Successfully loaded {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        traceback.print_exc()
        return data

# Load car data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'data')
car_data_path = os.path.join(data_dir, 'car_dataset.csv')

print(f"Current directory: {current_dir}")
print(f"Data directory: {data_dir}")
print(f"Car data path: {car_data_path}")

try:
    car_data = load_csv_data(car_data_path)
    # Convert year_start and year_end to integers
    for car in car_data:
        car['year_start'] = int(car['year_start'])
        car['year_end'] = int(car['year_end'])
    print(f"Car data loaded successfully: {len(car_data)} records")
except Exception as e:
    print(f"Error loading car data: {e}")
    traceback.print_exc()
    car_data = []

def validate_vehicle(plate: str, brand: str, model: str, year: int):
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

    return result

def main():
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    
    print(f"Validation data path: {validation_data_path}")
    
    # Load dataset
    try:
        validation_data = load_csv_data(validation_data_path)
        if not validation_data:
            print("No validation data loaded. Exiting.")
            return
        print(f"🔍 Running validation checks on {len(validation_data)} records...\n")
    except Exception as e:
        print(f"Error loading validation data: {e}")
        traceback.print_exc()
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
            traceback.print_exc()

if __name__ == "__main__":
    main()