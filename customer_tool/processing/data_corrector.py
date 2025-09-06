import os
import sys
import csv
import json
import logging
from datetime import datetime

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_validation_data(csv_path):
    """Load validation data from CSV."""
    validation_data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            validation_data.append(row)
    return validation_data

def save_validation_data(validation_data, csv_path):
    """Save validation data to CSV."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['user_input_plate', 'user_input_brand', 'user_input_model', 'user_input_year', 
                     'expected_brand', 'expected_model', 'expected_year', 'error_type']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in validation_data:
            writer.writerow(row)
    logger.info(f"Validation data saved to {csv_path}")

def correct_validation_data(validation_data, corrections):
    """Apply corrections to validation data."""
    corrected_data = []
    
    for i, row in enumerate(validation_data):
        correction = corrections[i] if i < len(corrections) else None
        
        if correction:
            # Create a new row with corrections applied
            corrected_row = row.copy()
            
            # Apply brand correction if available and there was a brand error
            if correction.get('suggested_brand') and 'typo_brand' in correction.get('errors', []):
                corrected_row['user_input_brand'] = correction['suggested_brand']
            
            # Apply model correction if available and there was a model error
            if correction.get('suggested_model') and 'typo_model' in correction.get('errors', []):
                corrected_row['user_input_model'] = correction['suggested_model']
            
            # Apply year correction if available and there was a year error
            if correction.get('valid_year_range') and 'invalid_year' in correction.get('errors', []):
                # Use the middle of the valid year range as a reasonable correction
                valid_start, valid_end = correction['valid_year_range']
                corrected_year = (valid_start + valid_end) // 2
                corrected_row['user_input_year'] = str(corrected_year)
            
            # Update error type
            remaining_errors = []
            if 'typo_brand' in correction.get('errors', []) and correction.get('suggested_brand'):
                pass  # Brand error fixed
            else:
                remaining_errors.append('typo_brand')
                
            if 'typo_model' in correction.get('errors', []) and correction.get('suggested_model'):
                pass  # Model error fixed
            else:
                remaining_errors.append('typo_model')
                
            if 'invalid_year' in correction.get('errors', []) and correction.get('valid_year_range'):
                pass  # Year error fixed
            else:
                remaining_errors.append('invalid_year')
                
            if 'plate_format_error' in correction.get('errors', []):
                remaining_errors.append('plate_format_error')
            
            # Update error type field
            if remaining_errors:
                corrected_row['error_type'] = ', '.join(remaining_errors)
            else:
                corrected_row['error_type'] = 'correct'
            
            corrected_data.append(corrected_row)
        else:
            corrected_data.append(row)
    
    return corrected_data

def main():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    corrected_data_path = os.path.join(data_dir, 'validation_dataset_corrected.csv')
    results_path = os.path.join(data_dir, 'validation_results.json')
    
    # Load validation data
    validation_data = load_validation_data(validation_data_path)
    logger.info(f"Loaded {len(validation_data)} validation records")
    
    # Load validation results
    with open(results_path, 'r', encoding='utf-8') as file:
        corrections = json.load(file)
    
    # Extract just the result part from each entry
    correction_results = [entry['result'] for entry in corrections]
    
    # Apply corrections
    corrected_data = correct_validation_data(validation_data, correction_results)
    
    # Save corrected data
    save_validation_data(corrected_data, corrected_data_path)
    logger.info(f"Corrected validation data saved to {corrected_data_path}")
    
    # Print comparison
    print("\n=== Validation Data Correction Results ===")
    print(f"Total records: {len(validation_data)}")
    
    # Count errors before and after
    errors_before = 0
    errors_after = 0
    
    for i, (original, corrected) in enumerate(zip(validation_data, corrected_data)):
        original_errors = original['error_type'].split(', ') if original['error_type'] != 'correct' else []
        corrected_errors = corrected['error_type'].split(', ') if corrected['error_type'] != 'correct' else []
        
        if original_errors and original_errors != ['']:
            errors_before += len(original_errors)
        
        if corrected_errors and corrected_errors != ['']:
            errors_after += len(corrected_errors)
        
        # Show changes
        if original != corrected:
            print(f"\nRecord {i}:")
            print(f"  Before: {original['user_input_brand']} {original['user_input_model']} {original['user_input_year']} (Errors: {original['error_type']})")
            print(f"  After:  {corrected['user_input_brand']} {corrected['user_input_model']} {corrected['user_input_year']} (Errors: {corrected['error_type']})")
    
    print(f"\nSummary:")
    print(f"  Total errors before correction: {errors_before}")
    print(f"  Total errors after correction: {errors_after}")
    print(f"  Errors fixed: {errors_before - errors_after}")
    print(f"  Error reduction: {((errors_before - errors_after) / errors_before * 100):.1f}%")

if __name__ == "__main__":
    main()