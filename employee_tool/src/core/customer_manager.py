# src/core/customer_manager.py
import os
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CustomerManager:
    """Manage customer data for the employee tool."""
    
    def __init__(self, data_file=None):
        """
        Initialize the customer manager.
        
        Args:
            data_file (str): Path to the customer data CSV file
        """
        from config.settings import CUSTOMER_DATA_PATH
        
        self.data_file = data_file or CUSTOMER_DATA_PATH
        self.customers = []
        self.load_customers()
    
    def load_customers(self):
        """Load customer data from CSV file."""
        if not os.path.exists(self.data_file):
            logger.warning(f"Customer data file not found: {self.data_file}")
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.customers = list(reader)
            
            logger.info(f"Loaded {len(self.customers)} customer records")
        except Exception as e:
            logger.error(f"Error loading customer data: {e}")
            self.customers = []
    
    def save_customers(self):
        """Save customer data to CSV file."""
        if not self.customers:
            logger.warning("No customer data to save")
            return
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8', newline='') as file:
                if self.customers:
                    writer = csv.DictWriter(file, fieldnames=self.customers[0].keys())
                    writer.writeheader()
                    writer.writerows(self.customers)
            
            logger.info(f"Saved {len(self.customers)} customer records")
        except Exception as e:
            logger.error(f"Error saving customer data: {e}")
    
    def get_customer(self, customer_id):
        """
        Get customer by ID.
        
        Args:
            customer_id (str): Customer ID
            
        Returns:
            dict: Customer data or None if not found
        """
        for customer in self.customers:
            if customer.get('customer_id') == customer_id:
                return customer
        return None
    
    def add_customer(self, customer_data):
        """
        Add a new customer.
        
        Args:
            customer_data (dict): Customer data
            
        Returns:
            bool: Success status
        """
        # Check if customer already exists
        customer_id = customer_data.get('customer_id')
        if self.get_customer(customer_id):
            logger.warning(f"Customer {customer_id} already exists")
            return False
        
        # Add created_at timestamp if not present
        if 'created_at' not in customer_data:
            customer_data['created_at'] = datetime.now().isoformat()
        
        self.customers.append(customer_data)
        self.save_customers()
        
        logger.info(f"Added new customer {customer_id}")
        return True
    
    def update_customer(self, customer_id, updated_data):
        """
        Update customer data.
        
        Args:
            customer_id (str): Customer ID
            updated_data (dict): Updated customer data
            
        Returns:
            bool: Success status
        """
        for i, customer in enumerate(self.customers):
            if customer.get('customer_id') == customer_id:
                # Update customer data
                self.customers[i].update(updated_data)
                
                # Add updated_at timestamp
                self.customers[i]['updated_at'] = datetime.now().isoformat()
                
                self.save_customers()
                
                logger.info(f"Updated customer {customer_id}")
                return True
        
        logger.warning(f"Customer {customer_id} not found for update")
        return False
    
    def search_customers(self, search_term, search_field='name'):
        """
        Search customers by a field.
        
        Args:
            search_term (str): Search term
            search_field (str): Field to search in
            
        Returns:
            list: Matching customers
        """
        results = []
        search_term = search_term.lower()
        
        for customer in self.customers:
            field_value = customer.get(search_field, '').lower()
            if search_term in field_value:
                results.append(customer)
        
        logger.info(f"Found {len(results)} customers matching '{search_term}' in {search_field}")
        return results
    
    def get_customers_by_vehicle(self, plate_number=None, brand=None, model=None):
        """
        Get customers by vehicle details.
        
        Args:
            plate_number (str): Vehicle plate number
            brand (str): Vehicle brand
            model (str): Vehicle model
            
        Returns:
            list: Matching customers
        """
        results = []
        
        for customer in self.customers:
            match = True
            
            if plate_number and customer.get('vehicle_plate', '').lower() != plate_number.lower():
                match = False
            
            if brand and customer.get('vehicle_brand', '').lower() != brand.lower():
                match = False
            
            if model and customer.get('vehicle_model', '').lower() != model.lower():
                match = False
            
            if match:
                results.append(customer)
        
        logger.info(f"Found {len(results)} customers matching vehicle criteria")
        return results