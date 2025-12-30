#!/usr/bin/env python3
"""
Mega da Virada 2025 - WEIGHTED ANALYSIS FOR ALL HISTORICAL DRAWS
Analyzes ALL draws with different weighting strategies based on recency
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


def main():
    """Main function for weighted analysis of all draws."""
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
    calculator.add_strategy('last_5_years', RecentOnlyStrategy(n_items=5, mode='years'))
    
    # Print header
    formatter.print_header(
        "MEGA DA VIRADA 2025 - WEIGHTED ANALYSIS",
        "ALL HISTORICAL DRAWS (1996-2025)"
    )
    
    # Load data
    print("\n⚙️  Loading ALL Mega Sena draws...")
    draws = data_loader.load_all_draws()
    
    # Reverse to have oldest first for proper weighting
    draws = list(reversed(draws))
    
    print(f"✓ Loaded {len(draws):,} historical draws")
    
    date_range = data_loader.get_date_range(draws)
    print(f"   Period: {date_range[0]} to {date_range[1]}")
    
    # Calculate all strategies
    print("\n⚙️  Calculating frequencies with different strategies...")
    results = calculator.calculate_all(draws)
    
    # Get simple frequency for comparison
    simple_freq = results['simple']
    
    # Display each strategy
    strategies_info = [
        ('simple', 'Simple Frequency', 'Equal weight for all years'),
        ('recent_exp', 'Recent Draws Weighted MORE (Exponential)', 
         'Recent draws count MUCH MORE (exponential growth)\nExample: 2025 draws have ~7x more weight than 1996 draws'),
        ('recent_linear', 'Recent Draws Weighted MORE (Linear)', 
         'Recent draws count MORE (linear growth)\nExample: 2025 draws have 4x more weight than 1996 draws'),
        ('older_more', 'Older Draws Weighted MORE (Historical Stability)', 
         'Older draws count MORE (exponential decay)\nExample: 1996 draws have ~7x more weight than 2025 draws'),
        ('last_5_years', 'Last 5 Years Only (2020-2025)', 
         'Only consider draws from the last 5 years'),
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
        "MEGA DA VIRADA 2025 - WEIGHTED ANALYSIS (ALL DRAWS)",
        "weighted_analysis_all_draws.txt"
    )
    
    # Print footer
    print("\n" + "=" * 70)
    print("  🍀 BOA SORTE NA MEGA DA VIRADA 2025! 🍀")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

