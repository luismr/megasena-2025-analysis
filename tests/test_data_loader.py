"""
Unit tests for data_loader module
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import MegaSenaDataLoader


class TestMegaSenaDataLoader:
    """Test cases for MegaSenaDataLoader class."""
    
    def test_init(self, temp_csv_file):
        """Test initialization of data loader."""
        loader = MegaSenaDataLoader(temp_csv_file)
        assert loader.csv_file == temp_csv_file
    
    def test_load_all_draws(self, temp_csv_file, sample_draws):
        """Test loading all draws from CSV."""
        loader = MegaSenaDataLoader(temp_csv_file)
        draws = loader.load_all_draws()
        
        assert len(draws) == len(sample_draws)
        assert draws[0]['Concurso'] == '1'
        assert draws[0]['Data'] == '11/03/1996'
    
    def test_load_all_draws_invalid_file(self):
        """Test loading with invalid file path."""
        loader = MegaSenaDataLoader('nonexistent_file.csv')
        
        with pytest.raises(SystemExit):
            loader.load_all_draws()
    
    def test_load_mega_virada_draws(self, temp_csv_file, sample_mega_virada_draws):
        """Test loading only Mega da Virada draws."""
        # Create a CSV with both regular and Mega da Virada draws
        import tempfile
        import csv
        
        all_draws = [
            {'Concurso': '100', 'Data': '15/03/1996', 
             'bola 1': '1', 'bola 2': '2', 'bola 3': '3',
             'bola 4': '4', 'bola 5': '5', 'bola 6': '6'},
        ] + sample_mega_virada_draws
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            fieldnames = ['Concurso', 'Data', 'bola 1', 'bola 2', 'bola 3', 
                          'bola 4', 'bola 5', 'bola 6']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_draws)
            temp_path = f.name
        
        try:
            loader = MegaSenaDataLoader(temp_path)
            virada_draws = loader.load_mega_virada_draws(start_year=2008)
            
            assert len(virada_draws) == 3
            assert all(draw['Data'].startswith('31/12/') for draw in virada_draws)
        finally:
            os.remove(temp_path)
    
    def test_load_mega_virada_draws_filter_by_year(self, sample_mega_virada_draws):
        """Test filtering Mega da Virada draws by start year."""
        import tempfile
        import csv
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            fieldnames = ['Concurso', 'Data', 'bola 1', 'bola 2', 'bola 3', 
                          'bola 4', 'bola 5', 'bola 6']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_mega_virada_draws)
            temp_path = f.name
        
        try:
            loader = MegaSenaDataLoader(temp_path)
            virada_draws = loader.load_mega_virada_draws(start_year=2010)
            
            assert len(virada_draws) == 1  # Only 2010 draw
        finally:
            os.remove(temp_path)
    
    def test_extract_numbers(self, sample_draws):
        """Test extracting numbers from a draw."""
        numbers = MegaSenaDataLoader.extract_numbers(sample_draws[0])
        
        assert len(numbers) == 6
        assert numbers == [10, 20, 30, 40, 50, 60]
    
    def test_extract_numbers_invalid_data(self):
        """Test extracting numbers with invalid data."""
        invalid_draw = {
            'bola 1': 'invalid',
            'bola 2': '20',
            'bola 3': '30',
            'bola 4': '40',
            'bola 5': '50',
            'bola 6': '60'
        }
        
        numbers = MegaSenaDataLoader.extract_numbers(invalid_draw)
        assert len(numbers) == 5  # Only 5 valid numbers
    
    def test_get_date_range(self, sample_draws):
        """Test getting date range from draws."""
        loader = MegaSenaDataLoader('dummy.csv')
        date_range = loader.get_date_range(sample_draws)
        
        assert date_range == ('11/03/1996', '25/03/1996')
    
    def test_get_date_range_empty(self):
        """Test getting date range with empty draws."""
        loader = MegaSenaDataLoader('dummy.csv')
        date_range = loader.get_date_range([])
        
        assert date_range == ('Unknown', 'Unknown')
    
    def test_load_draws_by_year_range(self, temp_csv_file):
        """Test loading draws within a year range."""
        loader = MegaSenaDataLoader(temp_csv_file)
        draws = loader.load_draws_by_year_range(1996, 1996)
        
        assert len(draws) == 3  # All sample draws are from 1996
    
    def test_ball_columns_constant(self):
        """Test that BALL_COLUMNS constant is correctly defined."""
        assert MegaSenaDataLoader.BALL_COLUMNS == [
            'bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6'
        ]

