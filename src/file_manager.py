#!/usr/bin/env python3
"""
File Manager Module
Single Responsibility: Handle file I/O operations for saving analysis results
"""

import os
from typing import Dict, List


class FileManager:
    """Responsible for saving analysis results to files."""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the file manager.
        
        Args:
            output_dir: Directory where output files will be saved
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_output_path(self, filename: str) -> str:
        """
        Get the full path for an output file.
        
        Args:
            filename: Name of the output file
        
        Returns:
            Full path to the output file
        """
        return os.path.join(self.output_dir, filename)
    
    def save_frequency_analysis(self, frequencies: Dict[int, float], 
                                  title: str, filename: str):
        """
        Save frequency analysis to a file.
        
        Args:
            frequencies: Dictionary of number frequencies
            title: Title for the analysis
            filename: Output filename
        """
        output_path = self.get_output_path(filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write("=" * 70 + "\n\n")
            f.write("Rank | Number | Frequency\n")
            f.write("-" * 30 + "\n")
            
            # Sort by frequency
            sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
            
            for i, (number, count) in enumerate(sorted_freq, 1):
                f.write(f"{i:4d} | {number:6d} | {count:9.2f}\n")
        
        print(f"✓ Analysis saved to: {output_path}")
        return output_path
    
    def save_complete_analysis(self, frequencies: Dict[int, float], 
                                 title: str, filename: str):
        """
        Save complete analysis including all 60 numbers.
        
        Args:
            frequencies: Dictionary of number frequencies
            title: Title for the analysis
            filename: Output filename
        """
        output_path = self.get_output_path(filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write("=" * 70 + "\n\n")
            f.write("Rank | Number | Frequency\n")
            f.write("-" * 30 + "\n")
            
            # Create complete list with all numbers 1-60
            all_numbers_list = []
            for num in range(1, 61):
                count = frequencies.get(num, 0)
                all_numbers_list.append((num, count))
            
            # Sort by frequency (descending), then by number (ascending)
            all_numbers_list.sort(key=lambda x: (-x[1], x[0]))
            
            for i, (number, count) in enumerate(all_numbers_list, 1):
                f.write(f"{i:4d} | {number:6d} | {count:9.2f}\n")
        
        print(f"✓ Complete analysis saved to: {output_path}")
        return output_path
    
    def save_strategy_comparison(self, all_strategies: Dict[str, List[int]], 
                                   consensus: List[int], title: str, filename: str):
        """
        Save comparison of multiple strategies.
        
        Args:
            all_strategies: Dictionary mapping strategy name to recommended numbers
            consensus: List of consensus recommendation numbers
            title: Title for the analysis
            filename: Output filename
        """
        output_path = self.get_output_path(filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write("=" * 70 + "\n\n")
            
            for i, (strategy_name, numbers) in enumerate(all_strategies.items(), 1):
                f.write(f"METHOD {i} - {strategy_name}:\n")
                formatted = ' - '.join([f'{n:02d}' for n in sorted(numbers)])
                f.write(f"   {formatted}\n\n")
            
            f.write("FINAL CONSENSUS BET:\n")
            formatted_consensus = ' - '.join([f'{n:02d}' for n in sorted(consensus)])
            f.write(f"   {formatted_consensus}\n")
        
        print(f"✓ Strategy comparison saved to: {output_path}")
        return output_path
    
    def save_mega_virada_detailed(self, draws: List[Dict[str, str]], 
                                    frequencies: Dict[int, float], 
                                    data_loader, filename: str):
        """
        Save detailed Mega da Virada analysis including all draws.
        
        Args:
            draws: List of draw dictionaries
            frequencies: Dictionary of number frequencies
            data_loader: MegaSenaDataLoader instance
            filename: Output filename
        """
        output_path = self.get_output_path(filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("MEGA DA VIRADA - DETAILED ANALYSIS (2008-2024)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("ALL DRAWS:\n")
            f.write("-" * 70 + "\n")
            
            for draw in draws:
                concurso = draw['Concurso']
                data = draw['Data']
                numbers = data_loader.extract_numbers(draw)
                sorted_nums = sorted(numbers)
                nums_str = ' - '.join([f'{n:02d}' for n in sorted_nums])
                f.write(f"{data} (Draw {concurso}): {nums_str}\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            f.write("NUMBER FREQUENCY - ALL 60 NUMBERS:\n")
            f.write("-" * 70 + "\n")
            f.write("Rank | Number | Frequency\n")
            f.write("-" * 30 + "\n")
            
            # Create complete list with all numbers 1-60
            all_numbers_list = []
            for num in range(1, 61):
                count = frequencies.get(num, 0)
                all_numbers_list.append((num, count))
            
            # Sort by frequency (descending), then by number (ascending)
            all_numbers_list.sort(key=lambda x: (-x[1], x[0]))
            
            for i, (number, count) in enumerate(all_numbers_list, 1):
                f.write(f"{i:4d} | {number:6d} | {count:9.0f}\n")
        
        print(f"✓ Detailed Mega da Virada analysis saved to: {output_path}")
        return output_path

