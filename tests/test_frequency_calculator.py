"""
Unit tests for frequency_calculator module
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.frequency_calculator import (
    FrequencyCalculator,
    SimpleFrequencyStrategy,
    WeightedFrequencyStrategy,
    RecentOnlyStrategy
)


class TestSimpleFrequencyStrategy:
    """Test cases for SimpleFrequencyStrategy."""
    
    def test_calculate(self, sample_draws):
        """Test simple frequency calculation."""
        strategy = SimpleFrequencyStrategy()
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        assert frequencies[10] == 3.0  # Appears in all 3 draws
        assert frequencies[20] == 3.0  # Appears in all 3 draws
        assert frequencies[30] == 3.0  # Appears in all 3 draws
        assert frequencies[5] == 1.0   # Appears in 1 draw
    
    def test_get_name(self):
        """Test strategy name."""
        strategy = SimpleFrequencyStrategy()
        assert strategy.get_name() == "Simple Frequency"
    
    def test_get_description(self):
        """Test strategy description."""
        strategy = SimpleFrequencyStrategy()
        assert "Equal weight" in strategy.get_description()


class TestWeightedFrequencyStrategy:
    """Test cases for WeightedFrequencyStrategy."""
    
    def test_calculate_recent_more(self, sample_draws):
        """Test weighted frequency with recent_more mode."""
        strategy = WeightedFrequencyStrategy('recent_more', decay_factor=2.0)
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        assert len(frequencies) > 0
        # Numbers from recent draws should have higher weights
    
    def test_calculate_recent_linear(self, sample_draws):
        """Test weighted frequency with recent_linear mode."""
        strategy = WeightedFrequencyStrategy('recent_linear')
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        assert len(frequencies) > 0
    
    def test_calculate_recent_less(self, sample_draws):
        """Test weighted frequency with recent_less mode."""
        strategy = WeightedFrequencyStrategy('recent_less', decay_factor=2.0)
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        assert len(frequencies) > 0
    
    def test_get_name_variants(self):
        """Test strategy names for different modes."""
        strategy_exp = WeightedFrequencyStrategy('recent_more')
        strategy_lin = WeightedFrequencyStrategy('recent_linear')
        strategy_old = WeightedFrequencyStrategy('recent_less')
        
        assert "Exponential" in strategy_exp.get_name()
        assert "Linear" in strategy_lin.get_name()
        assert "Older" in strategy_old.get_name()
    
    def test_calculate_weight_recent_more(self):
        """Test weight calculation for recent_more mode."""
        strategy = WeightedFrequencyStrategy('recent_more', decay_factor=2.0)
        
        weight_old = strategy._calculate_weight(0.0)
        weight_new = strategy._calculate_weight(1.0)
        
        assert weight_new > weight_old
    
    def test_calculate_weight_recent_less(self):
        """Test weight calculation for recent_less mode."""
        strategy = WeightedFrequencyStrategy('recent_less', decay_factor=2.0)
        
        weight_old = strategy._calculate_weight(0.0)
        weight_new = strategy._calculate_weight(1.0)
        
        assert weight_old > weight_new
    
    def test_calculate_weight_linear(self):
        """Test weight calculation for linear mode."""
        strategy = WeightedFrequencyStrategy('recent_linear')
        
        weight_old = strategy._calculate_weight(0.0)
        weight_mid = strategy._calculate_weight(0.5)
        weight_new = strategy._calculate_weight(1.0)
        
        assert weight_old < weight_mid < weight_new
        assert weight_old == 0.25
        assert weight_new == 1.0


class TestRecentOnlyStrategy:
    """Test cases for RecentOnlyStrategy."""
    
    def test_calculate_recent_draws(self, sample_draws):
        """Test calculation with recent draws only."""
        strategy = RecentOnlyStrategy(n_items=2, mode='draws')
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        # Should only consider last 2 draws
        assert frequencies[10] == 2.0
        assert frequencies[20] == 2.0
    
    def test_calculate_recent_years(self, sample_draws):
        """Test calculation with recent years only."""
        strategy = RecentOnlyStrategy(n_items=1, mode='years')
        frequencies = strategy.calculate(sample_draws)
        
        assert isinstance(frequencies, dict)
        # All sample draws are from 1996
        assert len(frequencies) > 0
    
    def test_get_name(self):
        """Test strategy name."""
        strategy = RecentOnlyStrategy(n_items=5, mode='draws')
        assert "Last 5" in strategy.get_name()
        assert "Draws" in strategy.get_name()
    
    def test_get_description(self):
        """Test strategy description."""
        strategy = RecentOnlyStrategy(n_items=3, mode='years')
        assert "3" in strategy.get_description()
        assert "years" in strategy.get_description()


class TestFrequencyCalculator:
    """Test cases for FrequencyCalculator."""
    
    def test_init(self):
        """Test initialization."""
        calculator = FrequencyCalculator()
        assert len(calculator.strategies) == 0
    
    def test_add_strategy(self):
        """Test adding a strategy."""
        calculator = FrequencyCalculator()
        strategy = SimpleFrequencyStrategy()
        
        calculator.add_strategy('simple', strategy)
        
        assert 'simple' in calculator.strategies
        assert calculator.strategies['simple'] == strategy
    
    def test_calculate_all(self, sample_draws):
        """Test calculating with all strategies."""
        calculator = FrequencyCalculator()
        calculator.add_strategy('simple', SimpleFrequencyStrategy())
        calculator.add_strategy('weighted', WeightedFrequencyStrategy('recent_more'))
        
        results = calculator.calculate_all(sample_draws)
        
        assert 'simple' in results
        assert 'weighted' in results
        assert isinstance(results['simple'], dict)
        assert isinstance(results['weighted'], dict)
    
    def test_get_top_numbers(self, sample_frequencies):
        """Test getting top numbers from frequencies."""
        calculator = FrequencyCalculator()
        top_numbers = calculator.get_top_numbers(sample_frequencies, n=5)
        
        assert len(top_numbers) == 5
        assert top_numbers[0] == (10, 100.0)  # Highest frequency
        assert top_numbers[1] == (20, 80.0)
        # Should be sorted in descending order
        for i in range(len(top_numbers) - 1):
            assert top_numbers[i][1] >= top_numbers[i + 1][1]
    
    def test_get_top_numbers_default_n(self, sample_frequencies):
        """Test getting top numbers with default n=8."""
        calculator = FrequencyCalculator()
        top_numbers = calculator.get_top_numbers(sample_frequencies)
        
        assert len(top_numbers) == 8
    
    def test_multiple_strategies(self, sample_draws):
        """Test using multiple strategies together."""
        calculator = FrequencyCalculator()
        calculator.add_strategy('simple', SimpleFrequencyStrategy())
        calculator.add_strategy('recent_exp', WeightedFrequencyStrategy('recent_more'))
        calculator.add_strategy('recent_lin', WeightedFrequencyStrategy('recent_linear'))
        calculator.add_strategy('recent_5', RecentOnlyStrategy(5, 'draws'))
        
        results = calculator.calculate_all(sample_draws)
        
        assert len(results) == 4
        assert all(isinstance(v, dict) for v in results.values())

