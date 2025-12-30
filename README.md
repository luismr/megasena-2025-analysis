# Mega Sena Analysis Tool

[![CI/CD Pipeline](https://github.com/luismr/megasena-2025-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/luismr/megasena-2025-analysis/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)](https://github.com/luismr/megasena-2025-analysis)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python tool for analyzing Mega Sena lottery draws with multiple prediction strategies. Refactored following **DRY (Don't Repeat Yourself)** and **SOLID** principles for maintainability and extensibility.

## 📁 Project Structure

```
megasena/
├── input/                          # Input data files
│   └── mega_sena_resultados.csv    # Historical Mega Sena draw results
├── output/                         # Generated analysis reports
│   ├── mega_virada_analysis.txt
│   ├── number_frequency_analysis.txt
│   ├── weighted_analysis_all_draws.txt
│   └── weighted_analysis_results.txt
├── src/                            # Core modules (following SOLID principles)
│   ├── __init__.py                 # Package initialization
│   ├── data_loader.py              # CSV data loading (Single Responsibility)
│   ├── frequency_calculator.py     # Frequency calculation strategies (Open/Closed)
│   ├── output_formatter.py         # Result formatting and display
│   └── file_manager.py             # File I/O operations
├── scripts/                        # Executable analysis scripts
│   ├── predict_all_draws.py        # Analyze all historical draws
│   ├── predict_mega_virada.py      # Analyze only Mega da Virada draws
│   ├── predict_weighted_all_draws.py      # Weighted analysis (all draws)
│   └── predict_weighted_mega_virada.py    # Weighted analysis (Mega da Virada)
└── README.md                       # This file
```

## 🎯 Features

### Core Modules (SOLID Design)

1. **`data_loader.py`** - Single Responsibility Principle
   - Load all Mega Sena draws
   - Filter Mega da Virada draws (Dec 31st)
   - Filter by year range
   - Extract numbers from draws

2. **`frequency_calculator.py`** - Open/Closed Principle
   - **Strategy Pattern** for extensibility
   - Multiple calculation strategies:
     - Simple frequency (equal weight)
     - Weighted by recency (exponential)
     - Weighted by recency (linear)
     - Weighted favoring older draws
     - Recent N years/draws only

3. **`output_formatter.py`** - Single Responsibility
   - Format and display analysis results
   - Pattern analysis (even/odd, low/high, sum)
   - Consensus analysis across strategies
   - Complete 60-number rankings

4. **`file_manager.py`** - Single Responsibility
   - Save frequency analysis
   - Save strategy comparisons
   - Save detailed reports
   - Manage output directory

## 🚀 Usage

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Running Analysis Scripts

All scripts should be run from the project root directory:

#### 1. Analyze All Historical Draws
```bash
python scripts/predict_all_draws.py
```
Analyzes all Mega Sena draws using simple frequency analysis.

**Output:** `output/number_frequency_analysis.txt`

#### 2. Analyze Mega da Virada Only
```bash
python scripts/predict_mega_virada.py
```
Analyzes only Mega da Virada draws (Dec 31st, 2008-2024) with pattern analysis.

**Output:** `output/mega_virada_analysis.txt`

#### 3. Weighted Analysis - All Draws
```bash
python scripts/predict_weighted_all_draws.py
```
Compares 5 different weighting strategies across all historical draws:
- Simple frequency
- Recent weighted more (exponential)
- Recent weighted more (linear)
- Older weighted more
- Last 5 years only

**Output:** `output/weighted_analysis_all_draws.txt`

#### 4. Weighted Analysis - Mega da Virada
```bash
python scripts/predict_weighted_mega_virada.py
```
Compares 5 different weighting strategies for Mega da Virada draws only.

**Output:** `output/weighted_analysis_results.txt`

## 🏗️ Architecture & Design Principles

### SOLID Principles Applied

#### **S - Single Responsibility Principle**
- Each module has one clear purpose:
  - `data_loader`: Load and filter data
  - `frequency_calculator`: Calculate frequencies
  - `output_formatter`: Format output
  - `file_manager`: Handle file I/O

#### **O - Open/Closed Principle**
- Easy to extend with new strategies without modifying existing code
- Add new `FrequencyStrategy` subclasses to introduce new calculation methods

#### **L - Liskov Substitution Principle**
- All `FrequencyStrategy` subclasses can be used interchangeably
- Consistent interface across all strategies

#### **I - Interface Segregation Principle**
- Small, focused interfaces
- Classes only depend on methods they use

#### **D - Dependency Inversion Principle**
- Scripts depend on abstract `FrequencyStrategy` interface
- Concrete implementations are injected at runtime

### DRY (Don't Repeat Yourself)

- **Before:** Each script duplicated CSV loading, frequency calculation, and output formatting
- **After:** Common functionality extracted into reusable modules
- **Result:** ~70% code reduction, easier maintenance

### Design Patterns Used

1. **Strategy Pattern** - `FrequencyStrategy` and subclasses
2. **Template Method** - Common analysis workflow in scripts
3. **Dependency Injection** - Strategies injected into `FrequencyCalculator`

## 📊 Analysis Strategies

### 1. Simple Frequency
Equal weight for all draws across history.

### 2. Weighted Frequency (Recent More - Exponential)
Recent draws have exponentially more weight (~7x for newest vs oldest).

### 3. Weighted Frequency (Recent More - Linear)
Recent draws have linearly more weight (~4x for newest vs oldest).

### 4. Weighted Frequency (Older More)
Older draws have more weight (favors historical stability).

### 5. Recent Only
Only considers the most recent N draws or years.

## 🔧 Extending the Tool

### Adding a New Frequency Strategy

1. Create a new class inheriting from `FrequencyStrategy`:

```python
from src.frequency_calculator import FrequencyStrategy

class MyCustomStrategy(FrequencyStrategy):
    def calculate(self, draws):
        # Your calculation logic
        return frequencies_dict
    
    def get_name(self):
        return "My Custom Strategy"
    
    def get_description(self):
        return "Description of what this does"
```

2. Add it to your script:

```python
calculator.add_strategy('my_custom', MyCustomStrategy())
```

### Adding a New Script

1. Create a new file in `scripts/`
2. Import the required modules from `src/`
3. Follow the existing script structure

## 🧪 Testing & CI/CD

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

### Test Coverage
- **55 unit tests** - 96% coverage
- **data_loader.py**: 98% | **file_manager.py**: 100% | **frequency_calculator.py**: 88% | **output_formatter.py**: 98%

### CI/CD Pipeline

**Automated on every push/PR:**
- ✅ **Tests** - Ubuntu, macOS, Windows × Python 3.9-3.12
- ✅ **Linting** - flake8, black, mypy
- ✅ **Coverage** - Automatic PR comments with detailed reports
- ✅ **Security** - Dependency & code scanning
- ✅ **Build** - Package validation

**GitHub Actions Workflows:**
- `ci.yml` - Main CI/CD pipeline (lint, test, coverage, build, security)
- `pr-comment.yml` - Coverage reports as PR comments
- `codeql.yml` - Security analysis
- `dependabot.yml` - Automatic dependency updates

**Coverage on PRs:**
Every PR gets an automatic comment with:
- Overall coverage % with color indicators (🟢 ≥90%, 🟡 ≥80%, 🟠 ≥70%, 🔴 <70%)
- Per-module breakdown
- Coverage trends

## 🤝 Contributing

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/luismr/megasena-2025-analysis.git
cd megasena-2025-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
pytest

# 4. Run scripts
python scripts/predict_all_draws.py
```

### Submit a Pull Request

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/megasena-2025-analysis.git
   cd megasena-2025-analysis
   ```

3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** and ensure quality:
   ```bash
   # Run tests
   pytest
   
   # Check coverage
   pytest --cov=src --cov-report=term-missing
   
   # Lint your code
   flake8 src/ scripts/
   
   # Format code
   black src/ scripts/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub
   - Go to the [main repository](https://github.com/luismr/megasena-2025-analysis)
   - Click "Pull Requests" → "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Submit!

### Contribution Guidelines

- ✅ Write tests for new features
- ✅ Maintain 90%+ code coverage
- ✅ Follow PEP 8 style guide
- ✅ Update documentation
- ✅ Use descriptive commit messages

### CI/CD Checks

Your PR will automatically run:
- Unit tests on multiple platforms
- Code coverage analysis
- Linting and formatting checks
- Security scans

A bot will comment with coverage report! 📊

## 📝 License

This is a personal analysis tool. Use at your own risk. Lottery is a game of chance.

## 🍀 Good Luck!

Remember: This tool is for educational and entertainment purposes. Past results do not guarantee future outcomes in random lottery draws.

---

**Boa Sorte na Mega da Virada 2025! 🎉**

