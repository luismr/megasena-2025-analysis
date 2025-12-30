"""
Unit tests for file_manager module
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.file_manager import FileManager
from src.data_loader import MegaSenaDataLoader


class TestFileManager:
    """Test cases for FileManager class."""
    
    def test_init(self, temp_output_dir):
        """Test initialization."""
        manager = FileManager(temp_output_dir)
        assert manager.output_dir == temp_output_dir
    
    def test_init_creates_directory(self):
        """Test that initialization creates output directory."""
        import tempfile
        import shutil
        
        temp_dir = os.path.join(tempfile.gettempdir(), 'test_megasena_output')
        
        # Ensure directory doesn't exist
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        manager = FileManager(temp_dir)
        
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_get_output_path(self, temp_output_dir):
        """Test getting output path."""
        manager = FileManager(temp_output_dir)
        path = manager.get_output_path('test.txt')
        
        expected = os.path.join(temp_output_dir, 'test.txt')
        assert path == expected
    
    def test_save_frequency_analysis(self, temp_output_dir, sample_frequencies, capsys):
        """Test saving frequency analysis."""
        manager = FileManager(temp_output_dir)
        
        output_path = manager.save_frequency_analysis(
            sample_frequencies,
            "TEST ANALYSIS",
            "test_freq.txt"
        )
        
        assert os.path.exists(output_path)
        
        # Read and verify content
        with open(output_path, 'r') as f:
            content = f.read()
            assert "TEST ANALYSIS" in content
            assert "Number" in content
            assert "Frequency" in content
            assert "10" in content  # Highest frequency number
        
        # Check console output
        captured = capsys.readouterr()
        assert "saved to" in captured.out
    
    def test_save_complete_analysis(self, temp_output_dir, sample_frequencies, capsys):
        """Test saving complete analysis with all 60 numbers."""
        manager = FileManager(temp_output_dir)
        
        output_path = manager.save_complete_analysis(
            sample_frequencies,
            "COMPLETE TEST ANALYSIS",
            "test_complete.txt"
        )
        
        assert os.path.exists(output_path)
        
        # Read and verify content
        with open(output_path, 'r') as f:
            content = f.read()
            assert "COMPLETE TEST ANALYSIS" in content
            
            # Should include all 60 numbers
            lines = content.split('\n')
            # Count data lines (excluding headers and separators)
            data_lines = [l for l in lines if l.strip() and 
                         not l.startswith('=') and 
                         not l.startswith('-') and
                         'Rank' not in l and
                         'COMPLETE' not in l]
            assert len(data_lines) >= 60
    
    def test_save_strategy_comparison(self, temp_output_dir, capsys):
        """Test saving strategy comparison."""
        manager = FileManager(temp_output_dir)
        
        all_strategies = {
            'Strategy 1': [10, 20, 30, 40, 50, 5, 15, 25],
            'Strategy 2': [5, 10, 15, 20, 25, 30, 35, 45],
            'Strategy 3': [10, 30, 33, 37, 42, 53, 54, 56]
        }
        consensus = [10, 20, 30, 5, 15, 25, 33, 37]
        
        output_path = manager.save_strategy_comparison(
            all_strategies,
            consensus,
            "STRATEGY COMPARISON TEST",
            "test_comparison.txt"
        )
        
        assert os.path.exists(output_path)
        
        # Read and verify content
        with open(output_path, 'r') as f:
            content = f.read()
            assert "STRATEGY COMPARISON TEST" in content
            assert "Strategy 1" in content
            assert "Strategy 2" in content
            assert "Strategy 3" in content
            assert "CONSENSUS" in content
            
            # Check formatting
            assert "05 -" in content or "05-" in content  # Numbers should have leading zeros
    
    def test_save_mega_virada_detailed(self, temp_output_dir, 
                                        sample_mega_virada_draws, capsys):
        """Test saving detailed Mega da Virada analysis."""
        manager = FileManager(temp_output_dir)
        loader = MegaSenaDataLoader('dummy.csv')
        
        frequencies = {
            10: 2.0,
            27: 1.0,
            40: 1.0,
            46: 1.0,
            49: 1.0,
            58: 1.0
        }
        
        output_path = manager.save_mega_virada_detailed(
            sample_mega_virada_draws,
            frequencies,
            loader,
            "test_virada.txt"
        )
        
        assert os.path.exists(output_path)
        
        # Read and verify content
        with open(output_path, 'r') as f:
            content = f.read()
            assert "MEGA DA VIRADA" in content
            assert "ALL DRAWS" in content
            assert "31/12/2008" in content
            assert "31/12/2009" in content
            assert "31/12/2010" in content
    
    def test_output_dir_exists(self, temp_output_dir):
        """Test that output directory is accessible."""
        manager = FileManager(temp_output_dir)
        assert os.path.exists(manager.output_dir)
        assert os.path.isdir(manager.output_dir)
    
    def test_multiple_saves_same_dir(self, temp_output_dir, sample_frequencies):
        """Test saving multiple files to the same directory."""
        manager = FileManager(temp_output_dir)
        
        path1 = manager.save_frequency_analysis(
            sample_frequencies, "Test 1", "file1.txt"
        )
        path2 = manager.save_frequency_analysis(
            sample_frequencies, "Test 2", "file2.txt"
        )
        
        assert os.path.exists(path1)
        assert os.path.exists(path2)
        assert path1 != path2
    
    def test_overwrite_existing_file(self, temp_output_dir, sample_frequencies):
        """Test overwriting an existing file."""
        manager = FileManager(temp_output_dir)
        
        # Save first time
        path1 = manager.save_frequency_analysis(
            sample_frequencies, "Version 1", "test.txt"
        )
        
        # Save again with different content
        path2 = manager.save_frequency_analysis(
            sample_frequencies, "Version 2", "test.txt"
        )
        
        assert path1 == path2
        
        # Read and verify it has new content
        with open(path2, 'r') as f:
            content = f.read()
            assert "Version 2" in content
            assert "Version 1" not in content

