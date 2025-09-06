import os
import sys
import json
import csv
import logging

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from core.validator import validate_vehicle
from utils.data_loader import load_csv_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def main():
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    output_path = os.path.join(data_dir, 'validation_results.json')
    
    # Validate batch from CSV
    results = validate_batch_from_csv(validation_data_path)
    
    # Save results to JSON
    save_results_to_json(results, output_path)
    
    # Print summary
    total_entries = len(results)
    errors_count = sum(1 for r in results if r["result"]["errors"])
    print(f"\nBatch Validation Summary:")
    print(f"Total entries processed: {total_entries}")
    print(f"Entries with errors: {errors_count}")
    print(f"Entries without errors: {total_entries - errors_count}")

if __name__ == "__main__":
    main()