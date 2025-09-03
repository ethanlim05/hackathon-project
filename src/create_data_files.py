import os
import csv

# Get the absolute path to the data directory
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'data')

# Create data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")

# Car dataset data
car_data = [
    {"brand": "Toyota", "model": "Vios", "year_start": "2010", "year_end": "2025"},
    {"brand": "Toyota", "model": "Camry", "year_start": "2005", "year_end": "2025"},
    {"brand": "Honda", "model": "City", "year_start": "2008", "year_end": "2025"},
    {"brand": "Honda", "model": "Civic", "year_start": "2000", "year_end": "2025"},
    {"brand": "Perodua", "model": "Myvi", "year_start": "2005", "year_end": "2025"},
    {"brand": "Perodua", "model": "Axia", "year_start": "2014", "year_end": "2025"},
    {"brand": "Proton", "model": "Saga", "year_start": "2000", "year_end": "2025"},
    {"brand": "Proton", "model": "X70", "year_start": "2019", "year_end": "2025"}
]

# Validation dataset data
validation_data = [
    {"user_input_plate": "BMR 3420", "user_input_brand": "Toyot", "user_input_model": "Vios", "user_input_year": "2021", "expected_brand": "Toyota", "expected_model": "Vios", "expected_year": "2021", "error_type": "typo_brand"},
    {"user_input_plate": "LQJ 4070", "user_input_brand": "Toyota", "user_input_model": "Camry", "user_input_year": "2015", "expected_brand": "Toyota", "expected_model": "Camry", "expected_year": "2015", "error_type": "correct"},
    {"user_input_plate": "SHX 7481", "user_input_brand": "Honda", "user_input_model": "Civicy", "user_input_year": "2001", "expected_brand": "Honda", "expected_model": "Civic", "expected_year": "2001", "error_type": "typo_model"},
    {"user_input_plate": "KJB 4513", "user_input_brand": "Toyot", "user_input_model": "Camr", "user_input_year": "2025", "expected_brand": "Toyota", "expected_model": "Camry", "expected_year": "2025", "error_type": "typo_brand, typo_model"},
    {"user_input_plate": "XUP 4254", "user_input_brand": "notorP", "user_input_model": "X70", "user_input_year": "2099", "expected_brand": "Proton", "expected_model": "X70", "expected_year": "2024", "error_type": "typo_brand, invalid_year"},
    {"user_input_plate": "RYL 5036", "user_input_brand": "Honda", "user_input_model": "City", "user_input_year": "2016", "expected_brand": "Honda", "expected_model": "City", "expected_year": "2016", "error_type": "correct"},
    {"user_input_plate": "EYU 1252", "user_input_brand": "Toyot", "user_input_model": "Vios", "user_input_year": "2011", "expected_brand": "Toyota", "expected_model": "Vios", "expected_year": "2011", "error_type": "typo_brand"},
    {"user_input_plate": "OUG9690", "user_input_brand": "Perodua", "user_input_model": "Axia", "user_input_year": "1800", "expected_brand": "Perodua", "expected_model": "Axia", "expected_year": "2015", "error_type": "invalid_year, plate_format_error"},
    {"user_input_plate": "BCN 8003", "user_input_brand": "Honda", "user_input_model": "Civic", "user_input_year": "2022", "expected_brand": "Honda", "expected_model": "Civic", "expected_year": "2022", "error_type": "typo_brand"},
    {"user_input_plate": "OLI 8161", "user_input_brand": "Honda", "user_input_model": "City", "user_input_year": "1970", "expected_brand": "Honda", "expected_model": "City", "expected_year": "2023", "error_type": "typo_model, invalid_year"}
]

# Write car dataset
car_dataset_path = os.path.join(data_dir, 'car_dataset.csv')
with open(car_dataset_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['brand', 'model', 'year_start', 'year_end']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(car_data)
print(f"Created car_dataset.csv with {len(car_data)} records")

# Write validation dataset
validation_dataset_path = os.path.join(data_dir, 'validation_dataset.csv')
with open(validation_dataset_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['user_input_plate', 'user_input_brand', 'user_input_model', 'user_input_year', 
                 'expected_brand', 'expected_model', 'expected_year', 'error_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(validation_data)
print(f"Created validation_dataset.csv with {len(validation_data)} records")

print("CSV files created successfully!")