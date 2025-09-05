# Smart Vehicle Data Validation & Error Detection

## Problem Statement
When buying or renewing car insurance online, users often mistype or enter incorrect vehicle details (e.g., plate number, car model, year of manufacture). These mistakes can delay policy approval, cause pricing errors, or even lead to invalid insurance coverage.

## Solution Overview
We built a smart backend system that detects and corrects typos or inaccurate vehicle input specifications in real-time. The system validates vehicle plate numbers, brands, models, and years of manufacture against a known dataset and provides suggestions for corrections.

## Key Features
- **Plate Number Validation**: Checks if the plate number follows the Malaysian plate format
- **Brand & Model Validation**: Detects typos in brand and model names using fuzzy matching
- **Year Validation**: Ensures the year of manufacture is within the valid range for the specific vehicle model
- **Error Detection**: Identifies and categorizes errors (typo_brand, typo_model, invalid_year, plate_format_error)
- **Suggestions**: Provides corrected suggestions for detected errors
- **Batch Processing**: Supports validation of multiple records at once
- **No External Dependencies**: Uses only Python's standard library for easy deployment
- **Unit Testing**: Comprehensive test suite to verify functionality
- **Logging**: Detailed logging for debugging and monitoring

## Project Structure

hackathon-project/
├── data/
│ ├── car_dataset.csv # Canonical dataset of valid vehicles
│ ├── validation_dataset.csv # Dataset for testing the validator
│ └── batch_validation_results.json # Results from batch validation
├── src/
│ ├── vehicle_validator.py # Main validation logic
│ ├── utils.py # Utility functions (fuzzy matching, plate validation)
│ ├── config.py # Configuration settings
│ ├── batch_validator.py # Validate multiple entries (batch processing)
│ ├── generate_report.py # Generate a summary report of validation results
│ ├── test_validator.py # Unit tests for the validator
│ └── validation.log # Log file (generated automatically)
└── README.md # This file

## Setup Instructions

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-project

2. Create and activate a virtual environment
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate

### Usage
1. To run the validator on the provided validation dataset and  see the results for each entry:
   cd src
   python vehicle_validator.py

2. To generate a summary report of the validation results on the test dataset:
   cd src
   python generate_report.py

3. To validate a single vehicle entry programmatically:
   cd src
   python -c "from vehicle_validator import validate_vehicle; print(validate_vehicle('ABC 1234', 'Toyot', 'Vios', '2021'))"

4. To validate multiple entries from the validation dataset and save results to JSON:
   cd src
   python batch_validator.py

5. To run the unit tests and verify all functionality:
   cd src
   python test_validator.py

### Data
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

### How it works
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

### Configuration
The system uses a configuration file (src/config.py) to manage settings:
- Data file paths
- Fuzzy matching thresholds
- Logging settings

### Logging
The system logs important events and errors to src/validation.log:
- Data loading operations
- Validation requests
- Errors and warnings
- Performance metrics