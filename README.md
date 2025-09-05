# Smart Vehicle Data Validation & Error Detection

## Overview
This project is a smart system designed to detect and correct typos or inaccurate vehicle input specifications in real-time. It's built for insurance applications to ensure smoother, faster, and more reliable insurance processing by identifying and fixing common data entry errors.


## Problem Statement
When buying or renewing car insurance online, users often mistype or enter incorrect vehicle details (e.g., plate number, car model, year of manufacture). These mistakes can delay policy approval, cause pricing errors, or even lead to invalid insurance coverage.

## Solution Overview
We built a smart backend system that detects and corrects typos or inaccurate vehicle input specifications in real-time. The system validates vehicle plate numbers, brands, models, and years of manufacture against a known dataset and provides suggestions for corrections.

## Key Features
1. Vehicle Data Validation
- Plate Number Validation: Checks if Malaysian license plate numbers follow the correct format (1-3 letters, optional space, 1-4 digits, optional trailing letter)
- Brand Name Validation: Detects typos in vehicle brands using fuzzy matching
- Model Name Validation: Identifies typos in vehicle models with fuzzy matching
- Year Validation: Verifies if the manufacturing year falls within the valid range for a specific brand and model
2. Error Detection Capabilities
- Detects common typos in brand names (e.g., "Toyot" instead of "Toyota")
- Identifies model name errors (e.g., "Civicy" instead of "Civic")
- Recognizes reversed brand names (e.g., "notorP" instead of "Proton")
- Flags invalid manufacturing years (outside the valid range)
- Identifies plate format errors
3. Data Correction
- Suggests corrections for detected errors
- Automatically applies corrections to datasets
- Provides confidence scores for suggested corrections
4. Batch Processing
- Processes multiple vehicle entries simultaneously
- Exports validation results to JSON format
- Generates summary statistics of validation results
5. Dataset Management
- Analyzes validation results to suggest dataset updates
- Adds new vehicle entries to the dataset
- Updates year ranges for existing vehicle models
- Creates backups before making changes
6. Testing Framework
- Includes unit tests for validation functionality
- Covers various error type scenarios

## Project Structure

## Project Structure

```text
hackathon-project/
├── data/
│   ├── car_dataset.csv              # Reference vehicle data
│   ├── validation_dataset.csv       # Dataset for validation
│   ├── test_dataset.csv             # Dataset for testing
│   └── validation_dataset_corrected.csv # Corrected dataset
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── validator.py             # Main validation logic
│   │   └── plate_validator.py       # Plate number validation
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── fuzzy_matcher.py         # Fuzzy matching logic
│   │   └── data_loader.py          # Data loading utilities
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration settings
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── batch_processor.py       # Batch processing logic
│   │   ├── data_corrector.py       # Data correction logic
│   │   └── dataset_updater.py      # Dataset update logic
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_validator.py       # Unit tests
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── full_workflow.py        # Complete workflow
│   ├── main.py                     # Main entry point
│   └── test_autocorrect.py         # Autocorrect demonstration
└── validation.log                  # Log file
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

### Testing
The project includes a comprehensive testing framework:
- Unit tests for all validation functions
- Test cases covering all error types
- Automated test execution with python main.py --mode test
