"""
Unit tests for output_formatter module
"""

import pytest
import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.output_formatter import ResultFormatter
from src.data_loader import MegaSenaDataLoader


class TestResultFormatter:
    """Test cases for ResultFormatter class."""
    
    def test_format_numbers_list(self):
        """Test formatting numbers list."""
        formatter = ResultFormatter()
        numbers = [5, 10, 33, 42]
        
        formatted = formatter.format_numbers_list(numbers)
        
        assert formatted == "05 - 10 - 33 - 42"
    
    def test_format_numbers_list_unsorted(self):
        """Test formatting with unsorted numbers."""
        formatter = ResultFormatter()
        numbers = [42, 5, 33, 10]
        
        formatted = formatter.format_numbers_list(numbers)
        
        # Should be sorted
        assert formatted == "05 - 10 - 33 - 42"
    
    def test_print_header(self, capsys):
        """Test printing header."""
        formatter = ResultFormatter()
        formatter.print_header("TEST TITLE", "Subtitle")
        
        captured = capsys.readouterr()
        assert "TEST TITLE" in captured.out
        assert "Subtitle" in captured.out
        assert "=" in captured.out
    
    def test_print_header_no_subtitle(self, capsys):
        """Test printing header without subtitle."""
        formatter = ResultFormatter()
        formatter.print_header("TEST TITLE")
        
        captured = capsys.readouterr()
        assert "TEST TITLE" in captured.out
        assert "=" in captured.out
    
    def test_print_section(self, capsys):
        """Test printing section."""
        formatter = ResultFormatter()
        formatter.print_section("Test Section")
        
        captured = capsys.readouterr()
        assert "Test Section" in captured.out
        assert "=" in captured.out
    
    def test_print_subsection(self, capsys):
        """Test printing subsection."""
        formatter = ResultFormatter()
        formatter.print_subsection("Test Subsection")
        
        captured = capsys.readouterr()
        assert "Test Subsection" in captured.out
        assert "-" in captured.out
    
    def test_display_draw_summary(self, capsys, sample_draws):
        """Test displaying draw summary."""
        formatter = ResultFormatter()
        date_range = ('11/03/1996', '25/03/1996')
        
        formatter.display_draw_summary(sample_draws, date_range)
        
        captured = capsys.readouterr()
        assert "3" in captured.out  # Number of draws
        assert "11/03/1996" in captured.out
        assert "25/03/1996" in captured.out
    
    def test_display_strategy_results(self, capsys, sample_frequencies):
        """Test displaying strategy results."""
        formatter = ResultFormatter()
        top_numbers = [(10, 100.0), (20, 80.0), (5, 70.0)]
        
        formatter.display_strategy_results(
            "Test Strategy",
            "Test description",
            top_numbers,
            sample_frequencies
        )
        
        captured = capsys.readouterr()
        assert "Test Strategy" in captured.out
        assert "Test description" in captured.out
        assert "Number 10" in captured.out
        assert "100.00" in captured.out
    
    def test_display_consensus_analysis(self, capsys, sample_frequencies):
        """Test displaying consensus analysis."""
        formatter = ResultFormatter()
        all_strategies = {
            'Strategy 1': [10, 20, 5, 30],
            'Strategy 2': [10, 20, 15, 25],
            'Strategy 3': [10, 30, 40, 50]
        }
        
        result = formatter.display_consensus_analysis(all_strategies, sample_frequencies)
        
        captured = capsys.readouterr()
        assert "CONSENSUS" in captured.out
        assert "Number 10" in captured.out  # Should appear in all 3
        assert isinstance(result, list)
        assert len(result) == 8
    
    def test_display_all_numbers_ranking(self, capsys, sample_frequencies):
        """Test displaying all numbers ranking."""
        formatter = ResultFormatter()
        total = sum(sample_frequencies.values())
        
        formatter.display_all_numbers_ranking(sample_frequencies, int(total))
        
        captured = capsys.readouterr()
        assert "COMPLETE RANKING" in captured.out
        assert "ALL 60 NUMBERS" in captured.out
        assert "|   10   |" in captured.out  # Highest frequency number should be in table
    
    def test_display_pattern_analysis(self, capsys, sample_draws):
        """Test displaying pattern analysis."""
        formatter = ResultFormatter()
        loader = MegaSenaDataLoader('dummy.csv')
        
        formatter.display_pattern_analysis(sample_draws, loader)
        
        captured = capsys.readouterr()
        assert "PATTERN ANALYSIS" in captured.out
        assert "Sum of 6 numbers" in captured.out
        assert "Even/Odd" in captured.out
        assert "Low" in captured.out
        assert "High" in captured.out
    
    def test_print_footer(self, capsys):
        """Test printing footer."""
        formatter = ResultFormatter()
        formatter.print_footer()
        
        captured = capsys.readouterr()
        assert "BOA SORTE" in captured.out or "GOOD LUCK" in captured.out
        assert "=" in captured.out
    
    def test_consensus_with_single_strategy(self, capsys, sample_frequencies):
        """Test consensus analysis with only one strategy."""
        formatter = ResultFormatter()
        all_strategies = {
            'Only Strategy': [10, 20, 5, 30, 15, 25, 40, 35]
        }
        
        result = formatter.display_consensus_analysis(all_strategies, sample_frequencies)
        
        assert len(result) == 8
        assert all(num in all_strategies['Only Strategy'] for num in result)
    
    def test_format_numbers_with_single_digit(self):
        """Test formatting single digit numbers."""
        formatter = ResultFormatter()
        numbers = [1, 2, 3]
        
        formatted = formatter.format_numbers_list(numbers)
        
        assert formatted == "01 - 02 - 03"
        # Verify leading zeros are present
        assert formatted.startswith("01")
        assert "02" in formatted
        assert "03" in formatted

