import re
import logging
import os
import sys

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

logger = logging.getLogger(__name__)

def validate_plate_format(plate: str):
    """
    Validate Malaysian plate format:
    - 1–3 letters
    - optional space
    - 1–4 digits
    - optional trailing letter
    """
    pattern = r"^[A-Z]{1,3}\s?[0-9]{1,4}[A-Z]?$"
    if not re.match(pattern, plate.upper()):
        return False, "plate_format_error"
    return True, None

if __name__ == "__main__":
    # Test the function
    print("Testing plate validation:")
    test_plates = ["ABC 1234", "XYZ123", "INVALID", "ABC1234A"]
    for plate in test_plates:
        valid, error = validate_plate_format(plate)
        print(f"{plate}: {'Valid' if valid else error}")