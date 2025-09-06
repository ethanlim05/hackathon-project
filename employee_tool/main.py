#!/usr/bin/env python3
"""
Employee-Facing Vehicle Data Validation Tool
Simplified command-line interface without API.
"""
import os
import sys
import csv
import argparse
import logging
from datetime import datetime

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

def setup_logging():
    """Set up logging for the application."""
    from config.settings import LOG_LEVEL, LOG_FILE
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
    return logger

def init_data_files():
    """Initialize data files if they don't exist."""
    from config.settings import (
        EMPLOYEE_CREDENTIALS_PATH,
        CUSTOMER_DATA_PATH,
        VEHICLE_GRANTS_PATH,
        CAR_DATA_PATH
    )
    
    # Create data directory if it doesn't exist
    data_dir = os.path.dirname(EMPLOYEE_CREDENTIALS_PATH)
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize employee credentials file
    if not os.path.exists(EMPLOYEE_CREDENTIALS_PATH):
        from core.auth import add_employee
        add_employee('admin', 'Administrator', 'admin123', 'admin')
        add_employee('validator1', 'Validator One', 'validator123', 'validator')
        add_employee('validator2', 'Validator Two', 'validator123', 'validator')
    
    # Initialize customer data file with headers and sample data
    if not os.path.exists(CUSTOMER_DATA_PATH) or os.path.getsize(CUSTOMER_DATA_PATH) == 0:
        with open(CUSTOMER_DATA_PATH, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'customer_id', 'name', 'email', 'phone', 'address',
                'vehicle_plate', 'vehicle_brand', 'vehicle_model', 'vehicle_year',
                'created_at', 'updated_at'
            ])
            
            # Add sample customer data
            writer.writerow([
                'CUST001', 'John Doe', 'john@example.com', '1234567890', '123 Main St',
                'ABC 1234', 'Toyota', 'Vios', '2021',
                datetime.now().isoformat(), ''
            ])
            writer.writerow([
                'CUST002', 'Jane Smith', 'jane@example.com', '0987654321', '456 Oak Ave',
                'XYZ 5678', 'Honda', 'Civic', '2020',
                datetime.now().isoformat(), ''
            ])
            writer.writerow([
                'CUST003', 'Robert Johnson', 'robert@example.com', '5551234567', '789 Pine Rd',
                'DEF 9012', 'Proton', 'X70', '2022',
                datetime.now().isoformat(), ''
            ])
    
    # Initialize vehicle grants file with headers and sample data
    if not os.path.exists(VEHICLE_GRANTS_PATH) or os.path.getsize(VEHICLE_GRANTS_PATH) == 0:
        with open(VEHICLE_GRANTS_PATH, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'grant_id', 'plate_number', 'brand', 'model', 'year',
                'owner_name', 'owner_id', 'grant_date', 'status',
                'added_by', 'added_at', 'updated_by', 'updated_at'
            ])
            
            # Add sample grant data
            writer.writerow([
                'GRANT001', 'ABC 1234', 'Toyota', 'Vios', '2021',
                'John Doe', 'CUST001', '2021-05-15', 'active',
                'admin', datetime.now().isoformat(), '', ''
            ])
            writer.writerow([
                'GRANT002', 'XYZ 5678', 'Honda', 'Civic', '2020',
                'Jane Smith', 'CUST002', '2020-08-20', 'active',
                'admin', datetime.now().isoformat(), '', ''
            ])
            writer.writerow([
                'GRANT003', 'DEF 9012', 'Proton', 'X70', '2022',
                'Robert Johnson', 'CUST003', '2022-01-10', 'active',
                'admin', datetime.now().isoformat(), '', ''
            ])
    
    # Create car_models_list.csv if it doesn't exist
    car_models_path = os.path.join(data_dir, 'car_models_list.csv')
    if not os.path.exists(car_models_path):
        with open(car_models_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['brand', 'model'])
            
            # Add car models from the dataset
            writer.writerow(['Toyota', 'Vios'])
            writer.writerow(['Toyota', 'Altis'])
            writer.writerow(['Toyota', 'Camry'])
            writer.writerow(['Honda', 'City'])
            writer.writerow(['Honda', 'Civic'])
            writer.writerow(['Perodua', 'Myvi'])
            writer.writerow(['Perodua', 'Axia'])
            writer.writerow(['Perodua', 'Bezza'])
            writer.writerow(['Proton', 'Saga'])
            writer.writerow(['Proton', 'X70'])
            writer.writerow(['Proton', 'Persona'])
            writer.writerow(['Proton', 'Iriz'])

def display_car_models():
    """Display the list of available car models."""
    from config.settings import DATA_DIR
    car_models_path = os.path.join(DATA_DIR, 'car_models_list.csv')
    
    print("\n=== Available Car Models ===")
    try:
        with open(car_models_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['brand']} {row['model']}")
    except Exception as e:
        print(f"Error loading car models: {e}")

def validate_vehicle_grant():
    """Validate a vehicle grant interactively."""
    from core.grant_validator import GrantValidator
    
    validator = GrantValidator()
    
    print("\n=== Vehicle Grant Validation ===")
    
    # Get input from user
    plate_number = input("Enter plate number: ")
    brand = input("Enter brand: ")
    model = input("Enter model: ")
    year = input("Enter year: ")
    owner_name = input("Enter owner name: ")
    owner_id = input("Enter owner ID: ")
    grant_date = input("Enter grant date (YYYY-MM-DD): ")
    
    # Create grant data
    grant_data = {
        'grant_id': f"GRANT{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'plate_number': plate_number,
        'brand': brand,
        'model': model,
        'year': year,
        'owner_name': owner_name,
        'owner_id': owner_id,
        'grant_date': grant_date
    }
    
    # Validate the grant
    result = validator.validate_grant(grant_data)
    
    # Display results
    print("\n=== Validation Results ===")
    print(f"Valid: {'Yes' if result['is_valid'] else 'No'}")
    
    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"- {error}")
    
    if result['warnings']:
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"- {warning}")
    
    if result['suggestions']:
        print("\nSuggestions:")
        for key, value in result['suggestions'].items():
            print(f"- {key}: {value}")
    
    # Ask if user wants to save the grant
    if result['is_valid'] or input("\nDo you want to save this grant anyway? (y/n): ").lower() == 'y':
        employee_id = input("Enter your employee ID: ")
        success, _ = validator.add_grant(grant_data, employee_id)
        
        if success:
            print("\nGrant saved successfully!")
        else:
            print("\nFailed to save grant.")

def search_vehicle_grants():
    """Search for vehicle grants interactively."""
    from core.grant_validator import GrantValidator
    
    validator = GrantValidator()
    
    print("\n=== Search Vehicle Grants ===")
    print("Search by:")
    print("1. Plate Number")
    print("2. Brand")
    print("3. Model")
    print("4. Owner Name")
    
    choice = input("Enter your choice (1-4): ")
    
    search_field = {
        '1': 'plate_number',
        '2': 'brand',
        '3': 'model',
        '4': 'owner_name'
    }.get(choice, 'plate_number')
    
    search_term = input(f"Enter {search_field.replace('_', ' ')}: ")
    
    grants = validator.search_grants(search_term, search_field)
    
    print(f"\nFound {len(grants)} grants:")
    
    for grant in grants:
        print("\n---")
        print(f"Grant ID: {grant.get('grant_id')}")
        print(f"Plate: {grant.get('plate_number')}")
        print(f"Vehicle: {grant.get('brand')} {grant.get('model')} ({grant.get('year')})")
        print(f"Owner: {grant.get('owner_name')} ({grant.get('owner_id')})")
        print(f"Date: {grant.get('grant_date')}")
        print(f"Status: {grant.get('status')}")

def generate_report():
    """Generate a simple report interactively."""
    from core.grant_validator import GrantValidator
    from core.customer_manager import CustomerManager
    
    grant_validator = GrantValidator()
    customer_manager = CustomerManager()
    
    print("\n=== Generate Report ===")
    print("1. Vehicle Grants Summary")
    print("2. Customer Summary")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == '1':
        # Vehicle grants summary
        grants = grant_validator.grant_data
        
        print("\n=== Vehicle Grants Summary ===")
        print(f"Total grants: {len(grants)}")
        
        # Count by brand
        brand_counts = {}
        for grant in grants:
            brand = grant.get('brand', 'Unknown')
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        print("\nGrants by Brand:")
        for brand, count in sorted(brand_counts.items()):
            print(f"- {brand}: {count}")
        
        # Count by status
        status_counts = {}
        for grant in grants:
            status = grant.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nGrants by Status:")
        for status, count in sorted(status_counts.items()):
            print(f"- {status}: {count}")
    
    elif choice == '2':
        # Customer summary
        customers = customer_manager.customers
        
        print("\n=== Customer Summary ===")
        print(f"Total customers: {len(customers)}")
        
        # Count by vehicle brand
        brand_counts = {}
        for customer in customers:
            brand = customer.get('vehicle_brand', 'Unknown')
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        print("\nCustomers by Vehicle Brand:")
        for brand, count in sorted(brand_counts.items()):
            print(f"- {brand}: {count}")
    
    else:
        print("Invalid choice.")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Employee-Facing Vehicle Data Validation Tool')
    parser.add_argument('--mode', choices=['init', 'cli'], 
                       default='cli', help='Mode of operation')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    if args.mode == 'init':
        logger.info("Initializing data files...")
        init_data_files()
        logger.info("Data files initialized successfully")
    elif args.mode == 'cli':
        logger.info("Starting employee tool...")
        init_data_files()
        
        # Main menu loop
        while True:
            print("\n=== Employee Vehicle Validation Tool ===")
            print("1. View Car Models")
            print("2. Validate Vehicle Grant")
            print("3. Search Vehicle Grants")
            print("4. Generate Report")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                display_car_models()
            elif choice == '2':
                validate_vehicle_grant()
            elif choice == '3':
                search_vehicle_grants()
            elif choice == '4':
                generate_report()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()