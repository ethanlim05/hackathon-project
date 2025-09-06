import os
import csv
import json
import logging
from collections import defaultdict, Counter
from datetime import datetime
from utils.data_loader import load_car_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_car_data(car_data_path):
    """Load car data from CSV."""
    car_data = []
    with open(car_data_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['year_start'] = int(row['year_start'])
            row['year_end'] = int(row['year_end'])
            car_data.append(row)
    return car_data

def save_car_data(car_data, car_data_path):
    """Save car data to CSV."""
    with open(car_data_path, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['brand', 'model', 'year_start', 'year_end']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for car in car_data:
            writer.writerow(car)
    logger.info(f"Car data saved to {car_data_path}")

def create_backup(car_data, backup_path):
    """Create a backup of the current car data."""
    with open(backup_path, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['brand', 'model', 'year_start', 'year_end']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for car in car_data:
            writer.writerow(car)
    logger.info(f"Backup created at {backup_path}")

def apply_updates(car_data, approved_updates):
    """Apply approved updates to car_data."""
    # Apply new entries
    for new_entry in approved_updates.get('new_entries', []):
        # Check if the entry already exists
        exists = any(
            car['brand'] == new_entry['brand'] and 
            car['model'] == new_entry['model'] 
            for car in car_data
        )
        
        if not exists:
            car_data.append({
                'brand': new_entry['brand'],
                'model': new_entry['model'],
                'year_start': new_entry['year_start'],
                'year_end': new_entry['year_end']
            })
            logger.info(f"Added new entry: {new_entry['brand']} {new_entry['model']} ({new_entry['year_start']}-{new_entry['year_end']})")
    
    # Apply year range updates
    for update in approved_updates.get('year_range_updates', []):
        for car in car_data:
            if car['brand'] == update['brand'] and car['model'] == update['model']:
                old_range = (car['year_start'], car['year_end'])
                new_range = update['suggested_range']
                
                car['year_start'] = new_range[0]
                car['year_end'] = new_range[1]
                
                logger.info(f"Updated year range for {car['brand']} {car['model']}: {old_range} -> {new_range}")
                break
    
    return car_data

def analyze_validation_results(results, car_data):
    """Analyze validation results to find potential updates to car_data."""
    # Track potential new entries and updates
    potential_new_entries = []
    potential_year_updates = defaultdict(list)
    
    # Count frequency of suggested corrections
    brand_model_counts = Counter()
    
    for entry in results:
        result = entry['result']
        input_data = entry['input']
        
        # If we have a suggested brand and model, count it
        if result['suggested_brand'] and result['suggested_model']:
            key = (result['suggested_brand'], result['suggested_model'])
            brand_model_counts[key] += 1
            
            # If the input had errors, this might be a new entry we should consider
            if result['errors']:
                # Check if this brand-model combination exists in our dataset
                exists = any(
                    car['brand'] == result['suggested_brand'] and 
                    car['model'] == result['suggested_model'] 
                    for car in car_data
                )
                
                if not exists:
                    # This is a potential new entry
                    potential_new_entries.append({
                        'brand': result['suggested_brand'],
                        'model': result['suggested_model'],
                        'year': input_data.get('year'),
                        'error_count': len(result['errors'])
                    })
        
        # Check for year range updates
        if result['suggested_brand'] and result['suggested_model'] and result['valid_year_range']:
            input_year = input_data.get('year')
            if input_year:
                try:
                    year_int = int(input_year)
                    valid_start, valid_end = result['valid_year_range']
                    
                    # If the year is outside the valid range but was suggested as a correction,
                    # we might need to expand our year range
                    if year_int < valid_start or year_int > valid_end:
                        key = (result['suggested_brand'], result['suggested_model'])
                        potential_year_updates[key].append(year_int)
                except ValueError:
                    pass
    
    # Generate suggestions
    suggestions = {
        'new_entries': [],
        'year_range_updates': [],
        'timestamp': datetime.now().isoformat()
    }
    
    # Filter potential new entries by frequency
    for (brand, model), count in brand_model_counts.items():
        if count >= 1:  # Threshold for suggesting new entries
            # Find the min and max years from potential entries
            related_entries = [e for e in potential_new_entries 
                              if e['brand'] == brand and e['model'] == model]
            
            if related_entries:
                years = [int(e['year']) for e in related_entries if e['year']]
                if years:
                    min_year = min(years)
                    max_year = max(years)
                    
                    suggestions['new_entries'].append({
                        'brand': brand,
                        'model': model,
                        'year_start': min_year,
                        'year_end': max_year,
                        'frequency': count,
                        'confidence': min(count / 10, 1.0)  # Simple confidence calculation
                    })
    
    # Generate year range update suggestions
    for (brand, model), years in potential_year_updates.items():
        if len(years) >= 1:  # Threshold for suggesting year updates
            min_year = min(years)
            max_year = max(years)
            
            # Find current year range
            current_range = None
            for car in car_data:
                if car['brand'] == brand and car['model'] == model:
                    current_range = (car['year_start'], car['year_end'])
                    break
            
            if current_range:
                # Only suggest if the new range is significantly different
                if min_year < current_range[0] - 1 or max_year > current_range[1] + 1:
                    suggestions['year_range_updates'].append({
                        'brand': brand,
                        'model': model,
                        'current_range': current_range,
                        'suggested_range': (min_year, max_year),
                        'frequency': len(years)
                    })
    
    return suggestions

def save_suggestions(suggestions, output_path):
    """Save suggestions to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(suggestions, file, indent=2)
    logger.info(f"Update suggestions saved to {output_path}")

def main():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'data')
    car_data_path = os.path.join(data_dir, 'car_dataset.csv')
    validation_results_path = os.path.join(data_dir, 'validation_results.json')
    suggestions_path = os.path.join(data_dir, 'dataset_update_suggestions.json')
    
    # Load car data
    car_data = load_car_data(car_data_path)
    
    # Load validation results
    with open(validation_results_path, 'r', encoding='utf-8') as file:
        results = json.load(file)
    
    # Analyze results
    suggestions = analyze_validation_results(results, car_data)
    
    # Save suggestions
    save_suggestions(suggestions, suggestions_path)
    
    # Print summary
    print("\n=== Dataset Update Suggestions ===")
    print(f"New entries to add: {len(suggestions['new_entries'])}")
    for entry in suggestions['new_entries']:
        print(f"  - {entry['brand']} {entry['model']} ({entry['year_start']}-{entry['year_end']}) - Confidence: {entry['confidence']:.2f}")
    
    print(f"\nYear range updates: {len(suggestions['year_range_updates'])}")
    for update in suggestions['year_range_updates']:
        print(f"  - {update['brand']} {update['model']}: {update['current_range']} -> {update['suggested_range']}")
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(data_dir, f'car_dataset_backup_{timestamp}.csv')
    create_backup(car_data, backup_path)
    
    # Load suggestions or create default if it doesn't exist
    if os.path.exists(suggestions_path):
        with open(suggestions_path, 'r', encoding='utf-8') as file:
            suggestions = json.load(file)
    else:
        logger.warning(f"Suggestions file not found at {suggestions_path}")
        logger.info("Creating default empty suggestions")
        suggestions = {
            'new_entries': [],
            'year_range_updates': [],
            'timestamp': datetime.now().isoformat()
        }
    
    # For this demo, we'll approve all suggestions with confidence >= 0.5
    # In a real system, this would be a manual review process
    approved_updates = {
        'new_entries': [e for e in suggestions.get('new_entries', []) if e.get('confidence', 0) >= 0.5],
        'year_range_updates': suggestions.get('year_range_updates', [])
    }
    
    # Apply updates
    car_data = apply_updates(car_data, approved_updates)
    
    # Save updated car data
    save_car_data(car_data, car_data_path)
    
    logger.info("Dataset updated successfully")

if __name__ == "__main__":
    main()