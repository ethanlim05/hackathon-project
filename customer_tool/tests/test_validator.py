import unittest
import os
import sys

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
sys.path.append(src_dir)

from core.validator import validate_vehicle

class TestVehicleValidator(unittest.TestCase):
    
    def test_valid_vehicle(self):
        """Test validation of a valid vehicle entry."""
        result = validate_vehicle("ABC 1234", "Toyota", "Vios", 2021)
        self.assertEqual(len(result["errors"]), 0)
    
    def test_typo_brand(self):
        """Test detection of brand typos."""
        result = validate_vehicle("ABC 1234", "Toyot", "Vios", 2021)
        self.assertIn("typo_brand", result["errors"])
        self.assertEqual(result["suggested_brand"], "Toyota")
    
    def test_typo_model(self):
        """Test detection of model typos."""
        result = validate_vehicle("ABC 1234", "Honda", "Civicy", 2021)
        self.assertIn("typo_model", result["errors"])
        self.assertEqual(result["suggested_model"], "Civic")
    
    def test_invalid_year(self):
        """Test detection of invalid years."""
        result = validate_vehicle("ABC 1234", "Toyota", "Vios", 1800)
        self.assertIn("invalid_year", result["errors"])
    
    def test_reversed_brand(self):
        """Test detection of reversed brand names."""
        result = validate_vehicle("ABC 1234", "notorP", "X70", 2021)
        self.assertIn("typo_brand", result["errors"])
        self.assertEqual(result["suggested_brand"], "Proton")
    
    def test_plate_format_error(self):
        """Test detection of plate format errors."""
        result = validate_vehicle("INVALID", "Toyota", "Vios", 2021)
        self.assertIn("plate_format_error", result["errors"])

def main():
    unittest.main()

if __name__ == "__main__":
    main()