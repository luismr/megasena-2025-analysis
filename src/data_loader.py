#!/usr/bin/env python3
"""
Data Loader Module
Single Responsibility: Handle CSV data loading operations
"""

import csv
import sys
from typing import List, Dict, Optional
from datetime import datetime


class MegaSenaDataLoader:
    """Responsible for loading and filtering Mega Sena draw data from CSV files."""
    
    BALL_COLUMNS = ['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']
    
    def __init__(self, csv_file: str):
        """
        Initialize the data loader.
        
        Args:
            csv_file: Path to the CSV file containing Mega Sena draw data
        """
        self.csv_file = csv_file
    
    def load_all_draws(self) -> List[Dict[str, str]]:
        """
        Load all draws from the CSV file.
        
        Returns:
            List of dictionaries containing draw data
        
        Raises:
            SystemExit: If file cannot be loaded
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                # Skip empty first line if present
                first_line = f.readline()
                if first_line.strip():
                    f.seek(0)  # Go back if first line wasn't empty
                
                reader = csv.DictReader(f)
                data = list(reader)
            
            return data
        except Exception as e:
            print(f"✗ Error loading file {self.csv_file}: {e}")
            sys.exit(1)
    
    def load_mega_virada_draws(self, start_year: int = 2008) -> List[Dict[str, str]]:
        """
        Load only Mega da Virada draws (December 31st).
        
        Args:
            start_year: First year to include (default: 2008)
        
        Returns:
            List of dictionaries containing Mega da Virada draw data
        """
        all_draws = self.load_all_draws()
        
        mega_virada_draws = []
        for row in all_draws:
            date = row.get('Data', '')
            if date.startswith('31/12/'):
                year = int(date.split('/')[-1])
                if year >= start_year:
                    mega_virada_draws.append(row)
        
        return mega_virada_draws
    
    def load_draws_by_year_range(self, start_year: int, end_year: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Load draws within a specific year range.
        
        Args:
            start_year: First year to include
            end_year: Last year to include (optional, defaults to current year)
        
        Returns:
            List of dictionaries containing draw data within the year range
        """
        if end_year is None:
            end_year = datetime.now().year
        
        all_draws = self.load_all_draws()
        
        filtered_draws = []
        for row in all_draws:
            date = row.get('Data', '')
            if date:
                year = int(date.split('/')[-1])
                if start_year <= year <= end_year:
                    filtered_draws.append(row)
        
        return filtered_draws
    
    @staticmethod
    def extract_numbers(draw: Dict[str, str]) -> List[int]:
        """
        Extract the 6 drawn numbers from a draw dictionary.
        
        Args:
            draw: Dictionary containing draw data
        
        Returns:
            List of 6 integers representing the drawn numbers
        """
        numbers = []
        for col in MegaSenaDataLoader.BALL_COLUMNS:
            try:
                number = int(draw[col])
                numbers.append(number)
            except (ValueError, KeyError):
                continue
        
        return numbers
    
    def get_date_range(self, draws: List[Dict[str, str]]) -> tuple:
        """
        Get the date range of the provided draws.
        
        Args:
            draws: List of draw dictionaries
        
        Returns:
            Tuple of (oldest_date, newest_date)
        """
        if not draws:
            return ('Unknown', 'Unknown')
        
        oldest = draws[0].get('Data', 'Unknown')
        newest = draws[-1].get('Data', 'Unknown')
        
        return (oldest, newest)

