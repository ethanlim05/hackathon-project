# src/core/grant_validator.py
import os
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GrantValidator:
    """Validate vehicle grant information."""
    
    def __init__(self, car_data_path=None, grants_data_path=None):
        """
        Initialize the grant validator.
        
        Args:
            car_data_path (str): Path to car data CSV file
            grants_data_path (str): Path to vehicle grants CSV file
        """
        from config.settings import CAR_DATA_PATH, VEHICLE_GRANTS_PATH
        
        self.car_data_path = car_data_path or CAR_DATA_PATH
        self.grants_data_path = grants_data_path or VEHICLE_GRANTS_PATH
        
        self.car_data = []
        self.grant_data = []
        
        self.load_car_data()
        self.load_grant_data()
    
    def load_car_data(self):
        """Load car data from CSV file."""
        if not os.path.exists(self.car_data_path):
            logger.warning(f"Car data file not found: {self.car_data_path}")
            return
        
        try:
            with open(self.car_data_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['year_start'] = int(row['year_start'])
                    row['year_end'] = int(row['year_end'])
                    self.car_data.append(row)
            
            logger.info(f"Loaded {len(self.car_data)} car records")
        except Exception as e:
            logger.error(f"Error loading car data: {e}")
            self.car_data = []
    
    def load_grant_data(self):
        """Load vehicle grant data from CSV file."""
        if not os.path.exists(self.grants_data_path):
            logger.warning(f"Vehicle grants file not found: {self.grants_data_path}")
            return
        
        try:
            with open(self.grants_data_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.grant_data = list(reader)
            
            logger.info(f"Loaded {len(self.grant_data)} vehicle grant records")
        except Exception as e:
            logger.error(f"Error loading vehicle grant data: {e}")
            self.grant_data = []
    
    def validate_grant(self, grant_data):
        """
        Validate vehicle grant information.
        
        Args:
            grant_data (dict): Grant data to validate
            
        Returns:
            dict: Validation result
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': {}
        }
        
        # Validate plate number format
        plate_number = grant_data.get('plate_number', '')
        if not self._validate_plate_format(plate_number):
            result['is_valid'] = False
            result['errors'].append('Invalid plate number format')
        
        # Validate vehicle details
        brand = grant_data.get('brand', '')
        model = grant_data.get('model', '')
        year = grant_data.get('year', '')
        
        try:
            year_int = int(year) if year else None
        except ValueError:
            year_int = None
            result['errors'].append('Invalid year format')
            result['is_valid'] = False
        
        # Check if brand and model exist in our database
        vehicle_exists = False
        for car in self.car_data:
            if car['brand'].lower() == brand.lower() and car['model'].lower() == model.lower():
                vehicle_exists = True
                
                # Check if year is within valid range
                if year_int and not (car['year_start'] <= year_int <= car['year_end']):
                    result['warnings'].append(f'Year {year} is outside the valid range for {brand} {model} ({car["year_start"]}-{car["year_end"]})')
                    result['suggestions']['valid_year_range'] = f"{car['year_start']}-{car['year_end']}"
                break
        
        if not vehicle_exists:
            result['warnings'].append(f'Vehicle {brand} {model} not found in database')
            
            # Try to find similar brands/models
            from utils.fuzzy_matcher import fuzzy_match
            
            brands = list(set(car['brand'] for car in self.car_data))
            matched_brand, brand_score = fuzzy_match(brand, brands)
            
            if matched_brand and brand_score > 70:
                result['suggestions']['brand'] = matched_brand
                
                # Try to match model within the suggested brand
                models = list(set(car['model'] for car in self.car_data if car['brand'] == matched_brand))
                matched_model, model_score = fuzzy_match(model, models)
                
                if matched_model and model_score > 70:
                    result['suggestions']['model'] = matched_model
        
        # Check for duplicate grants
        for grant in self.grant_data:
            if (grant.get('plate_number', '').lower() == plate_number.lower() and 
                grant.get('grant_id', '') != grant_data.get('grant_id', '')):
                result['warnings'].append(f'A grant with plate number {plate_number} already exists')
                break
        
        # Validate owner information
        owner_name = grant_data.get('owner_name', '')
        if not owner_name or len(owner_name.strip()) < 3:
            result['errors'].append('Invalid owner name')
            result['is_valid'] = False
        
        owner_id = grant_data.get('owner_id', '')
        if not owner_id or len(owner_id.strip()) < 5:
            result['errors'].append('Invalid owner ID')
            result['is_valid'] = False
        
        # Validate grant date
        grant_date = grant_data.get('grant_date', '')
        if grant_date:
            try:
                datetime.strptime(grant_date, '%Y-%m-%d')
            except ValueError:
                result['errors'].append('Invalid grant date format (use YYYY-MM-DD)')
                result['is_valid'] = False
        
        return result
    
    def _validate_plate_format(self, plate_number):
        """
        Validate Malaysian plate number format.
        
        Args:
            plate_number (str): Plate number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        import re
        
        # Malaysian plate format: 1-3 letters, optional space, 1-4 digits, optional trailing letter
        pattern = r"^[A-Z]{1,3}\s?[0-9]{1,4}[A-Z]?$"
        return bool(re.match(pattern, plate_number.upper()))
    
    def add_grant(self, grant_data, employee_id):
        """
        Add a new vehicle grant.
        
        Args:
            grant_data (dict): Grant data
            employee_id (str): ID of employee adding the grant
            
        Returns:
            tuple: (success, validation_result)
        """
        # Validate the grant data first
        validation_result = self.validate_grant(grant_data)
        
        if not validation_result['is_valid']:
            return False, validation_result
        
        # Add additional fields
        grant_data['added_by'] = employee_id
        grant_data['added_at'] = datetime.now().isoformat()
        grant_data['status'] = 'active'
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.grants_data_path), exist_ok=True)
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(self.grants_data_path)
        
        try:
            with open(self.grants_data_path, 'a', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=grant_data.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(grant_data)
            
            # Reload grant data
            self.load_grant_data()
            
            logger.info(f"Added new vehicle grant {grant_data.get('grant_id')} by employee {employee_id}")
            return True, validation_result
        except Exception as e:
            logger.error(f"Error adding vehicle grant: {e}")
            return False, {'is_valid': False, 'errors': [str(e)]}
    
    def update_grant(self, grant_id, updated_data, employee_id):
        """
        Update an existing vehicle grant.
        
        Args:
            grant_id (str): Grant ID to update
            updated_data (dict): Updated grant data
            employee_id (str): ID of employee updating the grant
            
        Returns:
            tuple: (success, validation_result)
        """
        # Find the grant
        grant_index = -1
        for i, grant in enumerate(self.grant_data):
            if grant.get('grant_id') == grant_id:
                grant_index = i
                break
        
        if grant_index == -1:
            logger.warning(f"Grant {grant_id} not found for update")
            return False, {'is_valid': False, 'errors': ['Grant not found']}
        
        # Create a copy of the grant with updated data
        updated_grant = self.grant_data[grant_index].copy()
        updated_grant.update(updated_data)
        
        # Validate the updated grant data
        validation_result = self.validate_grant(updated_grant)
        
        if not validation_result['is_valid']:
            return False, validation_result
        
        # Add audit fields
        updated_grant['updated_by'] = employee_id
        updated_grant['updated_at'] = datetime.now().isoformat()
        
        # Update the grant in our list
        self.grant_data[grant_index] = updated_grant
        
        # Save all grants back to file
        try:
            with open(self.grants_data_path, 'w', encoding='utf-8', newline='') as file:
                if self.grant_data:
                    writer = csv.DictWriter(file, fieldnames=self.grant_data[0].keys())
                    writer.writeheader()
                    writer.writerows(self.grant_data)
            
            logger.info(f"Updated vehicle grant {grant_id} by employee {employee_id}")
            return True, validation_result
        except Exception as e:
            logger.error(f"Error updating vehicle grant: {e}")
            return False, {'is_valid': False, 'errors': [str(e)]}
    
    def get_grant(self, grant_id):
        """
        Get a vehicle grant by ID.
        
        Args:
            grant_id (str): Grant ID
            
        Returns:
            dict: Grant data or None if not found
        """
        for grant in self.grant_data:
            if grant.get('grant_id') == grant_id:
                return grant
        return None
    
    def search_grants(self, search_term, search_field='plate_number'):
        """
        Search vehicle grants by a field.
        
        Args:
            search_term (str): Search term
            search_field (str): Field to search in
            
        Returns:
            list: Matching grants
        """
        results = []
        search_term = search_term.lower()
        
        for grant in self.grant_data:
            field_value = grant.get(search_field, '').lower()
            if search_term in field_value:
                results.append(grant)
        
        logger.info(f"Found {len(results)} grants matching '{search_term}' in {search_field}")
        return results