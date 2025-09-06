#!/usr/bin/env python3
"""
Smart Vehicle Data Validation & Error Detection
Main entry point for the application.
"""
import os
import sys
import argparse

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Smart Vehicle Data Validation & Error Detection')
    parser.add_argument('--mode', choices=['validate', 'batch', 'correct', 'workflow', 'test'], 
                       default='validate', help='Mode of operation')
    
    args = parser.parse_args()
    
    # Add src directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    if args.mode == 'validate':
        from core.validator import main as validate_main
        validate_main()
    elif args.mode == 'batch':
        from processing.batch_processor import main as batch_main
        batch_main()
    elif args.mode == 'correct':
        from processing.data_corrector import main as correct_main
        correct_main()
    elif args.mode == 'workflow':
        from workflows.full_workflow import main as workflow_main
        workflow_main()
    elif args.mode == 'test':
        from tests.test_validator import main as test_main
        test_main()

if __name__ == "__main__":
    main()