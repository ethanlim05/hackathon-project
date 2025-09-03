import os
import csv
from vehicle_validator import validate_vehicle

def validate_single_entry(plate, brand, model, year):
    """
    Validate a single vehicle entry and return the result.
    
    Args:
        plate (str): Vehicle plate number
        brand (str): Vehicle brand
        model (str): Vehicle model
        year (str/int): Year of manufacture
        
    Returns:
        dict: Validation result with suggestions and errors
    """
    # Convert year to integer
    try:
        year_int = int(year) if year else None
    except ValueError:
        year_int = None
    
    # Validate vehicle data
    result = validate_vehicle(plate, brand, model, year_int)
    
    return result

# Example usage
if __name__ == "__main__":
    # Test with a single entry
    result = validate_single_entry("ABC 1234", "Toyot", "Vios", "2021")
    print("Validation Result:")
    print(result)