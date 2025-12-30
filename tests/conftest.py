"""
Pytest configuration and fixtures
"""

import pytest
import os
import tempfile
import csv
from typing import List, Dict


@pytest.fixture
def sample_draws() -> List[Dict[str, str]]:
    """Fixture providing sample draw data for testing."""
    return [
        {
            'Concurso': '1',
            'Data': '11/03/1996',
            'bola 1': '10',
            'bola 2': '20',
            'bola 3': '30',
            'bola 4': '40',
            'bola 5': '50',
            'bola 6': '60'
        },
        {
            'Concurso': '2',
            'Data': '18/03/1996',
            'bola 1': '5',
            'bola 2': '10',
            'bola 3': '15',
            'bola 4': '20',
            'bola 5': '25',
            'bola 6': '30'
        },
        {
            'Concurso': '3',
            'Data': '25/03/1996',
            'bola 1': '10',
            'bola 2': '20',
            'bola 3': '30',
            'bola 4': '35',
            'bola 5': '45',
            'bola 6': '55'
        }
    ]


@pytest.fixture
def sample_mega_virada_draws() -> List[Dict[str, str]]:
    """Fixture providing sample Mega da Virada draw data."""
    return [
        {
            'Concurso': '1035',
            'Data': '31/12/2008',
            'bola 1': '1',
            'bola 2': '11',
            'bola 3': '26',
            'bola 4': '51',
            'bola 5': '59',
            'bola 6': '60'
        },
        {
            'Concurso': '1140',
            'Data': '31/12/2009',
            'bola 1': '10',
            'bola 2': '27',
            'bola 3': '40',
            'bola 4': '46',
            'bola 5': '49',
            'bola 6': '58'
        },
        {
            'Concurso': '1245',
            'Data': '31/12/2010',
            'bola 1': '2',
            'bola 2': '10',
            'bola 3': '34',
            'bola 4': '37',
            'bola 5': '43',
            'bola 6': '50'
        }
    ]


@pytest.fixture
def temp_csv_file(sample_draws) -> str:
    """Fixture that creates a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        fieldnames = ['Concurso', 'Data', 'bola 1', 'bola 2', 'bola 3', 
                      'bola 4', 'bola 5', 'bola 6']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_draws)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_output_dir():
    """Fixture that creates a temporary output directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_frequencies() -> Dict[int, float]:
    """Fixture providing sample frequency data."""
    return {
        10: 100.0,
        20: 80.0,
        5: 70.0,
        30: 65.0,
        15: 50.0,
        40: 45.0,
        25: 40.0,
        35: 35.0,
        50: 30.0,
        55: 25.0,
        60: 20.0,
        45: 15.0
    }

