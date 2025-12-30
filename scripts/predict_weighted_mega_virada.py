#!/usr/bin/env python3
"""
Mega da Virada 2025 - WEIGHTED TIME-BASED ANALYSIS
Analyzes Mega da Virada with different weighting strategies based on recency
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import MegaSenaDataLoader
from src.frequency_calculator import (
    FrequencyCalculator,
    SimpleFrequencyStrategy,
    WeightedFrequencyStrategy,
    RecentOnlyStrategy
)
from src.output_formatter import ResultFormatter
from src.file_manager import FileManager


def display_recent_draws_detail(draws: list, data_loader: MegaSenaDataLoader, n: int = 5):
    """Show the most recent draws for reference."""
    print("\n" + "=" * 70)
    print(f"  MOST RECENT {n} MEGA DA VIRADA DRAWS")
    print("=" * 70 + "\n")
    
    recent = draws[-n:] if len(draws) >= n else draws
    recent = list(reversed(recent))  # Show newest first
    
    for draw in recent:
        data = draw['Data']
        concurso = draw['Concurso']
        numbers = data_loader.extract_numbers(draw)
        sorted_nums = sorted(numbers)
        nums_str = ' - '.join([f'{n:02d}' for n in sorted_nums])
        print(f"   {data} (Draw {concurso}): {nums_str}")


def main():
    """Main function for weighted Mega da Virada analysis."""
    # Configuration
    csv_file = 'input/mega_sena_resultados.csv'
    
    # Initialize components
    data_loader = MegaSenaDataLoader(csv_file)
    calculator = FrequencyCalculator()
    formatter = ResultFormatter()
    file_manager = FileManager('output')
    
    # Add all strategies
    calculator.add_strategy('simple', SimpleFrequencyStrategy())
    calculator.add_strategy('recent_exp', WeightedFrequencyStrategy('recent_more', decay_factor=2.0))
    calculator.add_strategy('recent_linear', WeightedFrequencyStrategy('recent_linear'))
    calculator.add_strategy('older_more', WeightedFrequencyStrategy('recent_less', decay_factor=2.0))
    calculator.add_strategy('last_5_draws', RecentOnlyStrategy(n_items=5, mode='draws'))
    
    # Print header
    formatter.print_header(
        "MEGA DA VIRADA 2025 - WEIGHTED TIME-BASED ANALYSIS",
        "Comparing Different Weighting Strategies"
    )
    
    # Load Mega da Virada draws
    print("\n⚙️  Loading Mega da Virada draws (2008-2024)...")
    draws = data_loader.load_mega_virada_draws(start_year=2008)
    
    # Reverse to have oldest first for proper weighting
    draws = list(reversed(draws))
    
    print(f"✓ Loaded {len(draws)} Mega da Virada draws")
    
    # Show recent draws
    display_recent_draws_detail(draws, data_loader, 5)
    
    # Calculate all strategies
    print("\n⚙️  Calculating weighted frequencies with different strategies...")
    results = calculator.calculate_all(draws)
    
    # Get simple frequency for comparison
    simple_freq = results['simple']
    
    # Display each strategy
    strategies_info = [
        ('simple', 'Simple Frequency', 'Equal weight for all years'),
        ('recent_exp', 'Recent Draws Weighted MORE (Trending Numbers)', 
         'Recent years count MORE (exponential growth)\nExample: 2024 draws have ~7x more weight than 2008 draws'),
        ('recent_linear', 'Recent Draws Weighted MORE (Linear)', 
         'Recent draws count MORE (linear growth)\nExample: 2024 draws have 4x more weight than 2008 draws'),
        ('older_more', 'Older Draws Weighted MORE (Historical Stability)', 
         'Older years count MORE (exponential decay)\nExample: 2008 draws have ~7x more weight than 2024 draws'),
        ('last_5_draws', 'Last 5 Mega da Virada Draws Only', 
         'Only consider the most recent 5 Mega da Virada draws\nPeriod: Last 5 draws (2020-2024)'),
    ]
    
    all_recommendations = {}
    
    for key, name, description in strategies_info:
        top_numbers = calculator.get_top_numbers(results[key], n=8)
        formatter.display_strategy_results(name, description, top_numbers, simple_freq)
        all_recommendations[name] = [num for num, _ in top_numbers]
    
    # Consensus analysis
    consensus = formatter.display_consensus_analysis(all_recommendations, simple_freq)
    
    # Save results
    file_manager.save_strategy_comparison(
        all_recommendations,
        consensus,
        "MEGA DA VIRADA 2025 - WEIGHTED ANALYSIS RESULTS",
        "weighted_analysis_results.txt"
    )
    
    # Print footer
    print("\n" + "=" * 70)
    print("  🍀 BOA SORTE NA MEGA DA VIRADA 2025! 🍀")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

