#!/usr/bin/env python3
"""
Frequency Calculator Module
Single Responsibility: Calculate number frequencies using different strategies
Open/Closed Principle: Easy to extend with new calculation strategies
"""

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from typing import List, Dict
import math


class FrequencyStrategy(ABC):
    """Abstract base class for frequency calculation strategies."""
    
    @abstractmethod
    def calculate(self, draws: List[Dict[str, str]]) -> Dict[int, float]:
        """
        Calculate frequency scores for each number.
        
        Args:
            draws: List of draw dictionaries
        
        Returns:
            Dictionary mapping number to frequency score
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this strategy."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of this strategy."""
        pass


class SimpleFrequencyStrategy(FrequencyStrategy):
    """Calculate simple frequency with equal weight for all draws."""
    
    BALL_COLUMNS = ['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']
    
    def calculate(self, draws: List[Dict[str, str]]) -> Dict[int, float]:
        """Calculate simple frequency (no weighting)."""
        frequency_counter = Counter()
        
        for row in draws:
            for col in self.BALL_COLUMNS:
                try:
                    number = int(row[col])
                    frequency_counter[number] += 1
                except (ValueError, KeyError):
                    continue
        
        # Convert Counter to dict with float values
        return {num: float(count) for num, count in frequency_counter.items()}
    
    def get_name(self) -> str:
        return "Simple Frequency"
    
    def get_description(self) -> str:
        return "Equal weight for all draws"


class WeightedFrequencyStrategy(FrequencyStrategy):
    """Calculate weighted frequency based on recency."""
    
    BALL_COLUMNS = ['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']
    
    def __init__(self, weight_mode: str = 'recent_more', decay_factor: float = 2.0):
        """
        Initialize weighted frequency calculator.
        
        Args:
            weight_mode: 'recent_more', 'recent_linear', or 'recent_less'
            decay_factor: Factor controlling the strength of exponential weighting
        """
        self.weight_mode = weight_mode
        self.decay_factor = decay_factor
    
    def calculate(self, draws: List[Dict[str, str]]) -> Dict[int, float]:
        """Calculate weighted frequency based on recency."""
        weighted_scores = defaultdict(float)
        total_draws = len(draws)
        
        for draw_index, row in enumerate(draws):
            # Calculate weight based on position (0 = oldest, n-1 = newest)
            position = draw_index / (total_draws - 1) if total_draws > 1 else 0
            weight = self._calculate_weight(position)
            
            # Extract numbers and apply weight
            for col in self.BALL_COLUMNS:
                try:
                    number = int(row[col])
                    weighted_scores[number] += weight
                except (ValueError, KeyError):
                    continue
        
        return dict(weighted_scores)
    
    def _calculate_weight(self, position: float) -> float:
        """
        Calculate weight based on position and mode.
        
        Args:
            position: Position in the draw sequence (0 to 1)
        
        Returns:
            Weight value
        """
        if self.weight_mode == 'recent_more':
            # Exponential growth: recent draws have much more weight
            return math.exp(self.decay_factor * position) / math.exp(self.decay_factor)
        elif self.weight_mode == 'recent_linear':
            # Linear growth: recent draws have linearly more weight
            return 0.25 + (0.75 * position)  # Weight from 0.25 to 1.0
        else:  # recent_less
            # Exponential decay: older draws have more weight
            return math.exp(self.decay_factor * (1 - position)) / math.exp(self.decay_factor)
    
    def get_name(self) -> str:
        mode_names = {
            'recent_more': 'Recent Weighted MORE (Exponential)',
            'recent_linear': 'Recent Weighted MORE (Linear)',
            'recent_less': 'Older Weighted MORE'
        }
        return mode_names.get(self.weight_mode, 'Weighted Frequency')
    
    def get_description(self) -> str:
        mode_desc = {
            'recent_more': 'Recent draws have exponentially more weight',
            'recent_linear': 'Recent draws have linearly more weight',
            'recent_less': 'Older draws have exponentially more weight'
        }
        return mode_desc.get(self.weight_mode, 'Weighted by recency')


class RecentOnlyStrategy(FrequencyStrategy):
    """Calculate frequency for only the most recent N draws/years."""
    
    BALL_COLUMNS = ['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']
    
    def __init__(self, n_items: int = 5, mode: str = 'draws'):
        """
        Initialize recent-only frequency calculator.
        
        Args:
            n_items: Number of recent draws or years to consider
            mode: 'draws' or 'years'
        """
        self.n_items = n_items
        self.mode = mode
    
    def calculate(self, draws: List[Dict[str, str]]) -> Dict[int, float]:
        """Calculate frequency for only the most recent items."""
        frequency_counter = Counter()
        
        if self.mode == 'draws':
            # Take last N draws
            recent_draws = draws[-self.n_items:] if len(draws) >= self.n_items else draws
        else:  # years mode
            # Filter by year
            if draws:
                most_recent_date = draws[-1].get('Data', '')
                if most_recent_date:
                    most_recent_year = int(most_recent_date.split('/')[-1])
                    cutoff_year = most_recent_year - self.n_items + 1
                    
                    recent_draws = []
                    for row in draws:
                        date = row.get('Data', '')
                        if date:
                            year = int(date.split('/')[-1])
                            if year >= cutoff_year:
                                recent_draws.append(row)
                else:
                    recent_draws = draws
            else:
                recent_draws = draws
        
        for row in recent_draws:
            for col in self.BALL_COLUMNS:
                try:
                    number = int(row[col])
                    frequency_counter[number] += 1
                except (ValueError, KeyError):
                    continue
        
        return {num: float(count) for num, count in frequency_counter.items()}
    
    def get_name(self) -> str:
        return f"Last {self.n_items} {self.mode.title()} Only"
    
    def get_description(self) -> str:
        return f"Only consider the most recent {self.n_items} {self.mode}"


class FrequencyCalculator:
    """Main calculator that uses different strategies."""
    
    def __init__(self):
        """Initialize the frequency calculator."""
        self.strategies: Dict[str, FrequencyStrategy] = {}
    
    def add_strategy(self, key: str, strategy: FrequencyStrategy):
        """
        Add a calculation strategy.
        
        Args:
            key: Unique key for this strategy
            strategy: FrequencyStrategy instance
        """
        self.strategies[key] = strategy
    
    def calculate_all(self, draws: List[Dict[str, str]]) -> Dict[str, Dict[int, float]]:
        """
        Calculate frequencies using all registered strategies.
        
        Args:
            draws: List of draw dictionaries
        
        Returns:
            Dictionary mapping strategy key to frequency results
        """
        results = {}
        for key, strategy in self.strategies.items():
            results[key] = strategy.calculate(draws)
        
        return results
    
    def get_top_numbers(self, frequencies: Dict[int, float], n: int = 8) -> List[tuple]:
        """
        Get the top N numbers from frequency results.
        
        Args:
            frequencies: Dictionary of number frequencies
            n: Number of top numbers to return
        
        Returns:
            List of (number, score) tuples sorted by score
        """
        sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]

