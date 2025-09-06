# Smart Vehicle Data Validation & Error Detection

## Overview
This project is a comprehensive system designed to detect and correct typos or inaccurate vehicle input specifications in real-time. It consists of two complementary tools:

1. Customer-Facing Tool: A backend system that validates vehicle data entered by customers during insurance applications
2. Employee-Facing Tool: A command-line interface for employees to validate customer information, vehicle grants, and manage vehicle data

Both tools work together to ensure smoother, faster, and more reliable insurance processing by identifying and fixing common data entry errors.


## Problem Statement
When buying or renewing car insurance online, users often mistype or enter incorrect vehicle details (e.g., plate number, car model, year of manufacture). These mistakes can delay policy approval, cause pricing errors, or even lead to invalid insurance coverage.

## Solution Overview
We built a smart system with two components:

1. Customer-Facing Tool: A backend system that:
- Validates vehicle plate numbers, brands, models, and years of manufacture against a known dataset
- Provides suggestions for corrections in real-time
- Processes batch validations and generates reports

2. Employee-Facing Tool: A command-line interface that:
- Allows employees to validate vehicle grants interactively
- Provides a list of available car models for reference
- Enables searching and managing vehicle grant records
- Generates simple reports without external dependenci

## Key Features

# Customer Facing Tool
1. Vehicle Data Validation
- Plate Number Validation: Checks if Malaysian license plate numbers follow the correct format
- Brand Name Validation: Detects typos in vehicle brands using fuzzy matching
- Model Name Validation: Identifies typos in vehicle models with fuzzy matching
- Year Validation: Verifies if the manufacturing year falls within the valid range

2. Error Detection Capabilities
- Detects common typos in brand names (e.g., "Toyot" instead of "Toyota")
- Identifies model name errors (e.g., "Civicy" instead of "Civic")
- Recognizes reversed brand names (e.g., "notorP" instead of "Proton")
- Flags invalid manufacturing years and plate format errors

3. Data Correction
- Suggests corrections for detected errors
- Automatically applies corrections to datasets
- Provides confidence scores for suggested corrections

4. Batch Processing
- Processes multiple vehicle entries simultaneously
- Exports validation results to JSON format
- Generates summary statistics of validation results

# Employee-Facing Tool
1. Interactive Command-Line Interface
- Menu-driven system for easy navigation
- No external dependencies required
- Simple and intuitive for employee use

2. Vehicle Grant Management
- Validate vehicle grants with real-time feedback
- Search existing grants by various criteria
- Add new grants with validation

3. Car Model Reference
- Provides a list of all available car models
- Simple format following the dataset structure
- Easy to update and maintain

4. Reporting
- Generate simple reports on vehicle grants
- Customer summaries by vehicle brand
- Grant status summaries


## Project Structure

```text
project-root/
├── hackathon-project/              # Customer-facing tool
│   ├── data/
│   │   ├── car_dataset.csv         # Reference vehicle data
│   │   ├── validation_dataset.csv  # Dataset for validation
│   │   └── validation_dataset_corrected.csv # Corrected dataset
│   ├── src/
│   │   ├── core/
│   │   │   ├── validator.py        # Main validation logic
│   │   │   └── plate_validator.py  # Plate number validation
│   │   ├── utils/
│   │   │   ├── fuzzy_matcher.py    # Fuzzy matching logic
│   │   │   └── data_loader.py     # Data loading utilities
│   │   ├── config/
│   │   │   └── settings.py        # Configuration settings
│   │   ├── processing/
│   │   │   ├── batch_processor.py # Batch processing logic
│   │   │   ├── data_corrector.py  # Data correction logic
│   │   │   └── dataset_updater.py # Dataset update logic
│   │   ├── tests/
│   │   │   └── test_validator.py  # Unit tests
│   │   ├── workflows/
│   │   │   └── full_workflow.py   # Complete workflow
│   │   └── main.py               # Main entry point
│   └── validation.log            # Log file
│
└── employee_tool/                 # Employee-facing tool
    ├── data/
    │   ├── employee_credentials.csv # Employee authentication data
    │   ├── customer_data.csv       # Customer information
    │   ├── vehicle_grants.csv      # Vehicle grant records
    │   ├── car_models_list.csv    # List of available car models
    │   └── car_dataset.csv        # Copy of reference vehicle data
    ├── src/
    │   ├── core/
    │   │   ├── auth.py           # Employee authentication
    │   │   ├── customer_manager.py # Customer data management
    │   │   └── grant_validator.py # Vehicle grant validation
    │   ├── utils/
    │   │   ├── data_loader.py    # Data loading utilities
    │   │   └── fuzzy_matcher.py  # Fuzzy matching logic
    │   ├── config/
    │   │   └── settings.py       # Configuration settings
    │   └── cli/
    │       └── employee_cli.py   # Command-line interface
    ├── tests/
    │   └── test_employee_tool.py # Unit tests
    ├── main.py                   # Main entry point
    └── employee_tool.log        # Log file
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone <https://github.com/ethanlim05/hackathon-project.git>
   cd hackathon-project

2. Create and activate a virtual environment
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate

### Usage

# Customer-Facing Tool
1. Validate Mode (Runs the validator on the validation dataset and prints results.)
   python main.py --mode validate

2. Batch Mode (Processes the validation dataset in batch and saves results to JSON.)
   python main.py --mode batch

3. Correct Mode (Applies corrections to the validation dataset.)
   python main.py --mode correct

4. Workflow Mode (Runs the complete workflow (validate → correct → revalidate → compare).)
   python main.py --mode workflow

5. Test Mode (Runs the unit tests.)
   python main.py --mode test

# Employee-Facing Tool
1. Initialize Data Files (only need to do this once):
   python main.py --mode init

2. Start the CLI Tool:
   python main.py --mode cli

3. Use the Menu Options:
- View Car Models: See the list of available car models
- Validate Vehicle Grant: Enter vehicle details to validate
- Search Vehicle Grants: Search for existing grants
- Generate Report: Generate simple reports
- Exit: Exit the tool

### Data
# Customer-Facing Tool
1. car_dataset.csv
Contains the canonical dataset of valid vehicles with the following columns:

brand: Vehicle brand (e.g., Toyota, Honda)
model: Vehicle model (e.g., Vios, Civic)
year_start: First year the model was available
year_end: Last year the model was available (or projected)

2. validation_dataset.csv
Contains test data for the validator with the following columns:

user_input_plate: Input plate number
user_input_brand: Input brand
user_input_model: Input model
user_input_year: Input year
expected_brand: Expected corrected brand
expected_model: Expected corrected model
expected_year: Expected corrected year
error_type: Type of error(s) in the input

# Employee-Facing Tool
1. car_models_list.csv
Contains a simple list of available car models with columns:
- brand: Vehicle brand
- model: Vehicle model

2. employee_credentials.csv
Contains employee authentication data with columns:
- employee_id: Unique employee identifier
- name: Employee name
- password_hash: Hashed password
- role: Employee role (admin, validator)
- active: Account status
- created_at: Account creation timestamp

3. customer_data.csv
Contains customer information with columns:
- customer_id: Unique customer identifier
- name: Customer name
- email: Customer email
- phone: Customer phone number
- address: Customer address
- vehicle_plate: Vehicle plate number
- vehicle_brand: Vehicle brand
- vehicle_model: Vehicle model
- vehicle_year: Vehicle year
- created_at: Record creation timestamp
- updated_at: Record update timestamp

4. vehicle_grants.csv
Contains vehicle grant records with columns:
- grant_id: Unique grant identifier
- plate_number: Vehicle plate number
- brand: Vehicle brand
- model: Vehicle model
- year: Vehicle year
- owner_name: Vehicle owner name
- owner_id: Vehicle owner ID
- grant_date: Grant date
- status: Grant status
- added_by: Employee who added the grant
- added_at: Grant creation timestamp
- updated_by: Employee who last updated the grant
- updated_at: Grant update timestamp

### How it works
# Core Validation Logic
1. Plate Validation:
Uses a regular expression to check if the plate number follows the Malaysian format (1-3 letters, optional space, 1-4 digits, optional trailing letter).

2. Brand and Model Validation:
- Uses a custom implementation of the Levenshtein distance (edit distance) for fuzzy matching
- Compares the input brand and model against the canonical dataset
- Also handles reversed strings (e.g., "notorP" matches "Proton")

3. Year Validation:
- Checks if the input year is within the valid range for the specific vehicle model (from year_start to year_end)

4. Error Detection:
- Categorizes errors into: typo_brand, typo_model, invalid_year, plate_format_error, invalid_brand, invalid_model
- Returns a list of errors found and suggestions for correction

# Tool-Specific Implementation
- Customer-Facing Tool: Focuses on batch processing and automated corrections
- Employee-Facing Tool: Provides interactive validation with immediate feedback and manual override capabilities

### Error Types

The system can detect and classify the following types of errors:

- typo_brand: Typo in the brand name (e.g., "Toyot" → "Toyota")
- typo_model: Typo in the model name (e.g., "Civicy" → "Civic")
- invalid_year: Year outside the valid range for the model
- plate_format_error: Invalid plate number format
- invalid_brand: Brand not found in the database
- invalid_model: Model not found for the specified brand

### Performance Features
- Optimized Fuzzy Matching: Uses early termination in the Levenshtein distance calculation for better performance
- Efficient Data Structures: Uses sets for brand and model lookups for O(1) complexity
- Reversed String Handling: Special handling for reversed brand names (e.g., "notorP" → "Proton")
- No External Dependencies: Uses only Python's standard library for easy deployment
- Caching: Implements LRU caching for fuzzy matching to improve performance

### Configuration
# Customer-Facing Tool
- src/config/settings.py: Contains data file paths, fuzzy matching thresholds, and logging settings

# Employee-Facing Tool
- src/config/settings.py: Contains data file paths, validation thresholds, and logging settings

### Logging
# Customer-Facing Tool
- Logs to validation.log
- Records data loading operations, validation requests, errors, warnings, and performance metrics

# Employee-Facing Tool
- Logs to employee_tool.log
- Records authentication attempts, validation operations, data modifications, and system events

### Testing
# Customer-Facing Tool
- Unit tests for all validation functions in src/tests/test_validator.py
- Test cases covering all error types
- Automated test execution with python main.py --mode test

# Employee-Facing Tool
- Unit tests for employee tool functionality in tests/test_employee_tool.py
- Tests for authentication, validation, and data management
- Run tests with python -m unittest tests.test_employee_tool
