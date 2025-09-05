import os
import sys
import logging

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Add src directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, '..')
    sys.path.append(src_dir)
    
    # Import required modules
    from processing.batch_processor import validate_batch_from_csv, save_results_to_json
    from processing.data_corrector import load_validation_data, save_validation_data, correct_validation_data
    import json
    
    # Paths
    data_dir = os.path.join(src_dir, '..', 'data')
    original_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    corrected_data_path = os.path.join(data_dir, 'validation_dataset_corrected.csv')
    original_results_path = os.path.join(data_dir, 'original_validation_results.json')
    corrected_results_path = os.path.join(data_dir, 'corrected_validation_results.json')
    
    # Step 1: Validate original dataset
    logger.info("Step 1: Validating original dataset")
    original_results = validate_batch_from_csv(original_data_path)
    save_results_to_json(original_results, original_results_path)
    
    # Step 2: Correct the validation dataset
    logger.info("Step 2: Correcting validation dataset")
    validation_data = load_validation_data(original_data_path)
    correction_results = [entry['result'] for entry in original_results]
    corrected_data = correct_validation_data(validation_data, correction_results)
    save_validation_data(corrected_data, corrected_data_path)
    
    # Step 3: Validate corrected dataset
    logger.info("Step 3: Validating corrected dataset")
    corrected_results = validate_batch_from_csv(corrected_data_path)
    save_results_to_json(corrected_results, corrected_results_path)
    
    # Step 4: Compare results
    logger.info("Step 4: Comparing results")
    
    # Count errors in original
    original_errors = sum(len(entry['result']['errors']) for entry in original_results)
    corrected_errors = sum(len(entry['result']['errors']) for entry in corrected_results)
    
    print("\n=== Complete Workflow Results ===")
    print(f"Original dataset errors: {original_errors}")
    print(f"Corrected dataset errors: {corrected_errors}")
    print(f"Errors fixed: {original_errors - corrected_errors}")
    print(f"Error reduction: {((original_errors - corrected_errors) / original_errors * 100):.1f}%")
    
    # Show some examples
    print("\n=== Correction Examples ===")
    for i in range(min(5, len(validation_data))):
        original = validation_data[i]
        corrected = corrected_data[i]
        original_result = original_results[i]['result']
        corrected_result = corrected_results[i]['result']
        
        if original != corrected:
            print(f"\nRecord {i}:")
            print(f"  Input: {original['user_input_brand']} {original['user_input_model']} {original['user_input_year']}")
            print(f"  Original errors: {original_result['errors']}")
            print(f"  Corrected to: {corrected['user_input_brand']} {corrected['user_input_model']} {corrected['user_input_year']}")
            print(f"  Remaining errors: {corrected_result['errors']}")

if __name__ == "__main__":
    main()