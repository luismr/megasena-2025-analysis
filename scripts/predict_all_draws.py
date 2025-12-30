#!/usr/bin/env python3
"""
Mega da Virada 2025 - All Draws Analysis
Analyzes ALL historical Mega Sena draws using simple frequency analysis
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import MegaSenaDataLoader
from src.frequency_calculator import FrequencyCalculator, SimpleFrequencyStrategy
from src.output_formatter import ResultFormatter
from src.file_manager import FileManager


def main():
    """Main function for all draws analysis."""
    # Configuration
    csv_file = 'input/mega_sena_resultados.csv'
    
    # Initialize components
    data_loader = MegaSenaDataLoader(csv_file)
    calculator = FrequencyCalculator()
    formatter = ResultFormatter()
    file_manager = FileManager('output')
    
    # Add simple frequency strategy
    calculator.add_strategy('simple', SimpleFrequencyStrategy())
    
    # Print header
    formatter.print_header(
        "MEGA DA VIRADA 2025 - NUMBER PREDICTOR",
        "Based on ALL Historical Draws - Frequency Analysis"
    )
    
    # Load data
    print("\n⚙️  Loading ALL Mega Sena draws...")
    draws = data_loader.load_all_draws()
    print(f"✓ Loaded {len(draws):,} historical draws")
    
    date_range = data_loader.get_date_range(draws)
    formatter.display_draw_summary(draws, date_range)
    
    # Calculate frequencies
    print("\n⚙️  Analyzing number frequencies...")
    results = calculator.calculate_all(draws)
    simple_freq = results['simple']
    
    # Get top 8 numbers
    top_numbers = calculator.get_top_numbers(simple_freq, n=8)
    
    # Calculate statistics
    total_numbers_drawn = sum(simple_freq.values())
    avg_frequency = total_numbers_drawn / 60  # Mega Sena has numbers 1-60
    
    print(f"\n📊 Statistical Summary:")
    print(f"   • Total numbers drawn: {int(total_numbers_drawn):,}")
    print(f"   • Average frequency per number: {avg_frequency:.2f}")
    
    # Display results
    formatter.print_section("🎯 TOP 8 MOST FREQUENT NUMBERS")
    print("\nRecommended for your bet:")
    print("-" * 70)
    
    predicted_numbers = []
    for i, (number, count) in enumerate(top_numbers, 1):
        percentage = (count / total_numbers_drawn) * 100
        predicted_numbers.append(number)
        print(f"   {i}. Number {number:2d} - Drawn {int(count):4d} times ({percentage:.2f}%)")
    
    print("-" * 70)
    print(f"\n💰 YOUR BET FOR MEGA DA VIRADA 2025:")
    print(f"   {formatter.format_numbers_list(predicted_numbers)}")
    
    # Display complete ranking
    formatter.display_all_numbers_ranking(simple_freq, int(total_numbers_drawn))
    
    # Additional insights
    print(f"\n📈 Additional Insights:")
    least_common = sorted(simple_freq.items(), key=lambda x: x[1])[:8]
    least_numbers = [num for num, _ in least_common]
    print(f"   • Least frequent 8 numbers: {sorted(least_numbers)}")
    
    above_avg = [(num, count) for num, count in simple_freq.items() 
                 if count > avg_frequency]
    print(f"   • Numbers above average frequency ({avg_frequency:.0f}): {len(above_avg)}")
    
    # Save results
    file_manager.save_complete_analysis(
        simple_freq,
        "MEGA SENA - COMPLETE NUMBER FREQUENCY ANALYSIS (ALL DRAWS)",
        "number_frequency_analysis.txt"
    )
    
    # Print footer
    formatter.print_footer()


if __name__ == "__main__":
    main()

