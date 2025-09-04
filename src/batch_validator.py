import os
import csv
import json
from vehicle_validator import validate_vehicle

def validate_batch(entries):
    """
    Validate a batch of vehicle entries.
    
    Args:
        entries (list): List of dictionaries with vehicle data
        
    Returns:
        list: List of validation results
    """
    results = []
    
    for entry in entries:
        try:
            year = int(entry.get("year", "")) if entry.get("year") else None
        except ValueError:
            year = None
            
        result = validate_vehicle(
            plate=entry.get("plate", ""),
            brand=entry.get("brand", ""),
            model=entry.get("model", ""),
            year=year,
        )
        
        results.append({
            "input": entry,
            "result": result
        })
    
    return results

def validate_batch_from_csv(csv_path):
    """
    Validate vehicle entries from a CSV file.
    
    Args:
        csv_path (str): Path to CSV file
        
    Returns:
        list: List of validation results
    """
    entries = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entries.append({
                "plate": row.get("user_input_plate", ""),
                "brand": row.get("user_input_brand", ""),
                "model": row.get("user_input_model", ""),
                "year": row.get("user_input_year", "")
            })
    
    return validate_batch(entries)

def save_results_to_json(results, output_path):
    """
    Save validation results to a JSON file.
    
    Args:
        results (list): List of validation results
        output_path (str): Path to output JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=2)
    
    print(f"Results saved to {output_path}")

# Example usage
if __name__ == "__main__":
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    
    # Validate batch from CSV
    results = validate_batch_from_csv(validation_data_path)
    
    # Save results to JSON
    output_path = os.path.join(data_dir, 'validation_results.json')
    save_results_to_json(results, output_path)