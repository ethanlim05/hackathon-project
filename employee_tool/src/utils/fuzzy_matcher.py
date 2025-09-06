import os
import sys

# Add the parent directory to sys.path when run directly
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

import re
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Try to import configuration, use defaults if not available
try:
    from config.settings import FUZZY_MATCH_THRESHOLD
    logger.info("Loaded configuration from config.py")
except ImportError:
    logger.warning("config.py not found, using default thresholds")
    FUZZY_MATCH_THRESHOLD = 80

@lru_cache(maxsize=128)
def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings with caching.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        
        previous_row = current_row
    
    return previous_row[-1]

def fuzzy_match(query: str, choices: list, threshold: int = None) -> tuple:
    """
    Match user input to closest valid choice using Levenshtein distance.
    """
    if threshold is None:
        threshold = FUZZY_MATCH_THRESHOLD
        
    if not query or not choices:
        return None, 0
    
    query_lower = query.lower()
    best_match = None
    best_score = 0
    
    # Try normal matching first
    for choice in choices:
        choice_lower = choice.lower()
        distance = levenshtein_distance(query_lower, choice_lower)
        max_len = max(len(query), len(choice))
        similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
        
        if similarity >= threshold and similarity > best_score:
            best_match = choice
            best_score = similarity
            
            # Early termination if we find a perfect match
            if similarity == 100:
                return best_match, best_score
    
    # If no good match found, try reversed string
    if best_match is None:
        reversed_query = query[::-1].lower()
        
        for choice in choices:
            choice_lower = choice.lower()
            distance = levenshtein_distance(reversed_query, choice_lower)
            max_len = max(len(reversed_query), len(choice))
            similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
            
            if similarity >= threshold and similarity > best_score:
                best_match = choice
                best_score = similarity
                
                # Early termination if we find a perfect match
                if similarity == 100:
                    return best_match, best_score
    
    return best_match, best_score

if __name__ == "__main__":
    # Test the function
    print("Testing fuzzy_match function:")
    print(fuzzy_match("Toyota", ["Toyota", "Honda", "Proton"]))