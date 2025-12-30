"""
Mega Sena Analysis Package
Provides modules for analyzing Mega Sena lottery data.
"""

from .data_loader import MegaSenaDataLoader
from .frequency_calculator import (
    FrequencyCalculator,
    SimpleFrequencyStrategy,
    WeightedFrequencyStrategy,
    RecentOnlyStrategy
)
from .output_formatter import ResultFormatter
from .file_manager import FileManager

__all__ = [
    'MegaSenaDataLoader',
    'FrequencyCalculator',
    'SimpleFrequencyStrategy',
    'WeightedFrequencyStrategy',
    'RecentOnlyStrategy',
    'ResultFormatter',
    'FileManager'
]

