import os
import csv
from vehicle_validator import validate_vehicle

def generate_summary_report():
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    validation_data_path = os.path.join(data_dir, 'validation_dataset.csv')
    
    # Load validation dataset
    validation_data = []
    with open(validation_data_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            validation_data.append(row)
    
    # Initialize counters
    total_records = len(validation_data)
    correct_records = 0
    error_types = {
        'typo_brand': 0,
        'typo_model': 0,
        'invalid_year': 0,
        'plate_format_error': 0,
        'invalid_brand': 0,
        'invalid_model': 0
    }
    
    # Process each record
    for row in validation_data:
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
        
        # Count errors
        if not result["errors"]:
            correct_records += 1
        else:
            for error in result["errors"]:
                if error in error_types:
                    error_types[error] += 1
    
    # Generate report
    print("\n" + "="*50)
    print("VEHICLE VALIDATION SUMMARY REPORT")
    print("="*50)
    print(f"Total Records Processed: {total_records}")
    print(f"Correct Records: {correct_records} ({correct_records/total_records*100:.1f}%)")
    print(f"Records with Errors: {total_records - correct_records} ({(total_records - correct_records)/total_records*100:.1f}%)")
    print("\nError Type Distribution:")
    for error_type, count in error_types.items():
        if count > 0:
            print(f"- {error_type}: {count} ({count/total_records*100:.1f}%)")
    print("="*50)

if __name__ == "__main__":
    generate_summary_report()