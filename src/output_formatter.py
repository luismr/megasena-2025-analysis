#!/usr/bin/env python3
"""
Output Formatter Module
Single Responsibility: Format and display analysis results
"""

from typing import List, Dict, Set
from collections import Counter


class ResultFormatter:
    """Responsible for formatting and displaying analysis results."""
    
    @staticmethod
    def format_numbers_list(numbers: List[int]) -> str:
        """
        Format a list of numbers as a string with leading zeros.
        
        Args:
            numbers: List of numbers to format
        
        Returns:
            Formatted string like "01 - 02 - 03"
        """
        return ' - '.join([f'{n:02d}' for n in sorted(numbers)])
    
    @staticmethod
    def print_header(title: str, subtitle: str = ""):
        """Print a formatted header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        if subtitle:
            print(f"  {subtitle}")
        print("=" * 70)
    
    @staticmethod
    def print_section(title: str):
        """Print a section separator."""
        print("\n" + "=" * 70)
        print(f"{title}")
        print("=" * 70)
    
    @staticmethod
    def print_subsection(title: str):
        """Print a subsection separator."""
        print("\n" + "-" * 70)
        print(f"{title}")
        print("-" * 70)
    
    def display_draw_summary(self, draws: List[Dict[str, str]], date_range: tuple):
        """
        Display summary information about the draws.
        
        Args:
            draws: List of draw dictionaries
            date_range: Tuple of (oldest_date, newest_date)
        """
        print(f"\n📊 Statistical Summary:")
        print(f"   • Total draws analyzed: {len(draws):,}")
        print(f"   • Date range: {date_range[0]} to {date_range[1]}")
    
    def display_strategy_results(self, strategy_name: str, description: str, 
                                  top_numbers: List[tuple], simple_freq: Dict[int, float] = None):
        """
        Display results for a single strategy.
        
        Args:
            strategy_name: Name of the strategy
            description: Description of the strategy
            top_numbers: List of (number, score) tuples
            simple_freq: Optional simple frequency data for comparison
        """
        self.print_section(f"📊 {strategy_name}")
        if description:
            print(f"\nStrategy: {description}")
        
        print("\nTop 8 Numbers:")
        for i, (num, score) in enumerate(top_numbers, 1):
            if simple_freq and num in simple_freq:
                freq = int(simple_freq[num])
                print(f"   {i}. Number {num:2d} - Score: {score:6.2f} (appeared {freq}x total)")
            else:
                print(f"   {i}. Number {num:2d} - Score: {score:6.2f}")
        
        numbers = [num for num, _ in top_numbers]
        print(f"\n💰 Recommended: {self.format_numbers_list(numbers)}")
    
    def display_consensus_analysis(self, all_strategies: Dict[str, List[int]], 
                                     simple_freq: Dict[int, float] = None):
        """
        Display consensus analysis showing numbers appearing in multiple strategies.
        
        Args:
            all_strategies: Dictionary mapping strategy name to list of recommended numbers
            simple_freq: Optional simple frequency data for additional context
        """
        self.print_section("🎯 CONSENSUS ANALYSIS")
        print("Numbers appearing in multiple methods")
        
        # Convert to sets
        strategy_sets = {key: set(nums) for key, nums in all_strategies.items()}
        all_numbers = set().union(*strategy_sets.values())
        
        # Count occurrences
        number_counts = {}
        for num in all_numbers:
            count = sum(1 for s in strategy_sets.values() if num in s)
            number_counts[num] = count
        
        # Group by count
        by_count = {}
        for num, count in number_counts.items():
            if count not in by_count:
                by_count[count] = []
            by_count[count].append(num)
        
        # Display from highest to lowest consensus
        for count in sorted(by_count.keys(), reverse=True):
            stars = "⭐" * count
            nums = sorted(by_count[count])
            print(f"\n{stars} In {count} method(s) ({len(nums)} numbers):")
            print(f"   {nums}")
        
        # Create final consensus ranking
        print("\n" + "-" * 70)
        print("Consensus Ranking (by number of methods):")
        
        consensus_ranking = sorted(
            number_counts.items(),
            key=lambda x: (x[1], simple_freq.get(x[0], 0) if simple_freq else 0),
            reverse=True
        )
        
        for num, methods_count in consensus_ranking[:15]:
            stars = "⭐" * methods_count
            freq_str = ""
            if simple_freq and num in simple_freq:
                freq = int(simple_freq[num])
                freq_str = f", appeared {freq}x total"
            print(f"   {stars} Number {num:2d} - In {methods_count} method(s){freq_str}")
        
        # Final recommendation
        final_bet = sorted([num for num, _ in consensus_ranking[:8]])
        print(f"\n💰 FINAL CONSENSUS BET (Top 8):")
        print(f"   {self.format_numbers_list(final_bet)}")
        
        return final_bet
    
    def display_all_numbers_ranking(self, frequencies: Dict[int, float], 
                                      total_numbers_drawn: int):
        """
        Display complete ranking of all 60 numbers.
        
        Args:
            frequencies: Dictionary of number frequencies
            total_numbers_drawn: Total count of all numbers drawn
        """
        self.print_section("📋 COMPLETE RANKING - ALL 60 NUMBERS")
        
        # Create complete list with all numbers 1-60
        all_numbers_list = []
        for num in range(1, 61):
            count = frequencies.get(num, 0)
            all_numbers_list.append((num, count))
        
        # Sort by frequency (descending), then by number (ascending)
        all_numbers_list.sort(key=lambda x: (-x[1], x[0]))
        
        # Display in a grid format
        print("\nRank | Number | Times | %    | Rank | Number | Times | %")
        print("-" * 70)
        
        mid_point = 30
        for i in range(mid_point):
            num1, count1 = all_numbers_list[i]
            pct1 = (count1 / total_numbers_drawn) * 100 if total_numbers_drawn > 0 else 0
            
            if i + mid_point < len(all_numbers_list):
                num2, count2 = all_numbers_list[i + mid_point]
                pct2 = (count2 / total_numbers_drawn) * 100 if total_numbers_drawn > 0 else 0
                print(f" {i+1:2d}  |   {num1:2d}   | {int(count1):4d}  |{pct1:4.1f}% "
                      f"| {i+mid_point+1:2d}  |   {num2:2d}   | {int(count2):4d}  |{pct2:4.1f}%")
            else:
                print(f" {i+1:2d}  |   {num1:2d}   | {int(count1):4d}  |{pct1:4.1f}% |")
        
        print("-" * 70)
    
    def display_pattern_analysis(self, draws: List[Dict[str, str]], 
                                   data_loader):
        """
        Display pattern analysis for draws.
        
        Args:
            draws: List of draw dictionaries
            data_loader: MegaSenaDataLoader instance for extracting numbers
        """
        self.print_section("📊 PATTERN ANALYSIS")
        
        patterns = {
            'sum_range': [],
            'even_odd': [],
            'low_high': [],  # Low: 1-30, High: 31-60
        }
        
        for row in draws:
            numbers = data_loader.extract_numbers(row)
            
            if len(numbers) == 6:
                # Sum
                total = sum(numbers)
                patterns['sum_range'].append(total)
                
                # Even/Odd
                even = sum(1 for n in numbers if n % 2 == 0)
                odd = 6 - even
                patterns['even_odd'].append((even, odd))
                
                # Low/High
                low = sum(1 for n in numbers if n <= 30)
                high = 6 - low
                patterns['low_high'].append((low, high))
        
        # Display sum analysis
        if patterns['sum_range']:
            avg_sum = sum(patterns['sum_range']) / len(patterns['sum_range'])
            min_sum = min(patterns['sum_range'])
            max_sum = max(patterns['sum_range'])
            print(f"\n📊 Sum of 6 numbers:")
            print(f"   • Average: {avg_sum:.0f}")
            print(f"   • Range: {min_sum} to {max_sum}")
        
        # Display even/odd analysis
        if patterns['even_odd']:
            even_odd_counter = Counter(patterns['even_odd'])
            print(f"\n🔢 Even/Odd distribution:")
            for (even, odd), count in sorted(even_odd_counter.items(), 
                                              key=lambda x: x[1], reverse=True):
                print(f"   • {even} even / {odd} odd: {count} times")
        
        # Display low/high analysis
        if patterns['low_high']:
            low_high_counter = Counter(patterns['low_high'])
            print(f"\n📈 Low (1-30) / High (31-60) distribution:")
            for (low, high), count in sorted(low_high_counter.items(), 
                                              key=lambda x: x[1], reverse=True):
                print(f"   • {low} low / {high} high: {count} times")
    
    @staticmethod
    def print_footer():
        """Print a footer message."""
        print("\n" + "=" * 70)
        print("  🍀 BOA SORTE! GOOD LUCK! 🍀")
        print("=" * 70 + "\n")

