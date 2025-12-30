#!/usr/bin/env python3
"""
Mega da Virada 2025 - SPECIAL ANALYSIS
Analyzes ONLY the Mega da Virada draws (December 31st) from 2008 to 2024
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import MegaSenaDataLoader
from src.frequency_calculator import FrequencyCalculator, SimpleFrequencyStrategy
from src.output_formatter import ResultFormatter
from src.file_manager import FileManager


def display_all_draws(draws: list, data_loader: MegaSenaDataLoader):
    """Display all Mega da Virada draws."""
    print("\n" + "=" * 70)
    print("  ALL MEGA DA VIRADA DRAWS (2008-2024)")
    print("=" * 70 + "\n")
    
    for draw in draws:
        concurso = draw['Concurso']
        data = draw['Data']
        numbers = data_loader.extract_numbers(draw)
        sorted_nums = sorted(numbers)
        nums_str = ' - '.join([f'{n:02d}' for n in sorted_nums])
        print(f"   {data} (Draw {concurso}): {nums_str}")
    
    print("\n" + "-" * 70)


def main():
    """Main function for Mega da Virada analysis."""
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
        "MEGA DA VIRADA 2025 - SPECIAL PREDICTOR",
        "Analyzing ONLY Mega da Virada Draws (2008-2024)"
    )
    
    # Load Mega da Virada draws
    print("\n⚙️  Loading Mega da Virada draws (Dec 31st, 2008-2024)...")
    draws = data_loader.load_mega_virada_draws(start_year=2008)
    print(f"✓ Loaded {len(draws)} Mega da Virada draws")
    
    # Display all draws
    display_all_draws(draws, data_loader)
    
    # Calculate frequencies
    print("\n⚙️  Analyzing number frequencies...")
    results = calculator.calculate_all(draws)
    simple_freq = results['simple']
    
    # Analyze patterns
    print("⚙️  Analyzing patterns...")
    formatter.display_pattern_analysis(draws, data_loader)
    
    # Get top 8 numbers
    top_numbers = calculator.get_top_numbers(simple_freq, n=8)
    
    # Calculate statistics
    total_numbers_drawn = sum(simple_freq.values())
    expected_per_number = total_numbers_drawn / 60
    
    # Display results
    formatter.print_section("MEGA DA VIRADA 2025 - SPECIAL PREDICTION")
    print("Based on Mega da Virada History (2008-2024)")
    
    print(f"\n📊 Statistical Summary:")
    print(f"   • Mega da Virada draws analyzed: {len(draws)}")
    print(f"   • Total numbers drawn: {int(total_numbers_drawn)}")
    print(f"   • Years covered: 2008-2024 ({len(draws)} years)")
    print(f"   • Expected frequency per number: {expected_per_number:.2f}")
    
    formatter.print_subsection("🎯 TOP 8 MOST FREQUENT NUMBERS IN MEGA DA VIRADA")
    
    predicted_numbers = []
    for i, (number, count) in enumerate(top_numbers, 1):
        percentage = (count / total_numbers_drawn) * 100
        predicted_numbers.append(number)
        deviation = count - expected_per_number
        symbol = "↑" if deviation > 0 else "↓"
        print(f"   {i}. Number {number:2d} - Drawn {int(count):2d} times ({percentage:.1f}%) {symbol}")
    
    print("-" * 70)
    print(f"\n💰 YOUR BET FOR MEGA DA VIRADA 2025:")
    print(f"   {formatter.format_numbers_list(predicted_numbers)}")
    
    # Display complete ranking
    formatter.display_all_numbers_ranking(simple_freq, int(total_numbers_drawn))
    
    # Show hot numbers
    print(f"\n⭐ Numbers that appeared 3+ times in Mega da Virada:")
    hot_numbers = [(num, count) for num, count in simple_freq.items() if count >= 3]
    hot_numbers.sort(key=lambda x: x[1], reverse=True)
    if hot_numbers:
        hot_nums_list = [f"{num}({int(count)}x)" for num, count in hot_numbers]
        print(f"   {', '.join(hot_nums_list)}")
    else:
        print("   None")
    
    # Show numbers that never appeared
    all_numbers = set(range(1, 61))
    drawn_numbers = set(simple_freq.keys())
    never_drawn = sorted(all_numbers - drawn_numbers)
    
    if never_drawn:
        print(f"\n❌ Numbers NEVER drawn in Mega da Virada ({len(never_drawn)} numbers):")
        print(f"   {', '.join([str(n) for n in never_drawn])}")
    
    # Save detailed analysis
    file_manager.save_mega_virada_detailed(
        draws, simple_freq, data_loader,
        "mega_virada_analysis.txt"
    )
    
    # Print footer
    print("\n" + "=" * 70)
    print("  🍀 BOA SORTE NA MEGA DA VIRADA 2025! 🍀")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

