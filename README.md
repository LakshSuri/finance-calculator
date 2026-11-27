# Finance Calculator

A modular Python application for compound growth calculations,
periodic contribution modeling, financial goal calculations,
and educational financial mathematics.

The project explores the time value of money through
deterministic mathematical models and interactive
visualizations.

## Overview

| Component | Current Implementation |
|---|---|
| Financial calculation functions | 3 |
| Visualization types | 3 |
| Automated test cases | 3 |
| Calculation history | Local file storage |
| Application interface | Command line |

## Core Features

| Feature | Description |
|---|---|
| Investment Growth | Models the compound growth of an initial principal |
| Monthly Contributions | Calculates accumulated value from periodic contributions |
| Financial Goal Planner | Calculates the periodic contribution required to reach a hypothetical target |
| Calculation History | Records completed calculations locally |
| Growth Visualization | Displays annual changes in calculated balances |
| Scenario Comparison | Compares growth under different assumed return rates |

## Contents

- [Quick Start](#quick-start)
- [Mathematical Framework](#mathematical-framework)
- [Project Architecture](#project-architecture)
- [Python Examples](#python-examples)
- [Automated Testing](#automated-testing)
- [Limitations](#limitations)
- [Future Development](#future-development)
- [Related Projects](#related-projects)

## Quick Start

### Installation

Clone the repository:

```bash
git clone https://github.com/LakshSuri/finance-calculator.git
cd finance-calculator
```

Create an isolated Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install matplotlib pytest
```

### Running the Application

```bash
python main.py
```

The interactive menu provides access to six operations,
including financial calculations, calculation history,
visualizations, and application termination.

## Mathematical Framework

### Compound Growth

The future value of an initial principal under a constant
annual growth rate is:

```math
FV=P(1+r)^t
```

| Variable | Definition |
|---|---|
| P | Initial principal |
| r | Annual effective growth rate |
| t | Number of years |
| FV | Calculated future value |

### Periodic Contributions

The accumulated value of equal monthly contributions is
calculated using the future value of an ordinary annuity:

```math
FV=C\frac{(1+i)^n-1}{i}
```

where:

```math
i=\frac{r}{12}
```

```math
n=12t
```

| Variable | Definition |
|---|---|
| C | Monthly contribution |
| r | Nominal annual rate |
| i | Monthly periodic rate |
| n | Total number of contributions |

Contributions are assumed to occur at the end of each
month.

When the periodic rate is zero, the expression reduces to:

```math
FV=Cn
```

### Financial Goal Calculations

Rearranging the ordinary annuity formula produces the
required periodic contribution for a hypothetical target:

```math
C=\frac{FV\cdot i}{(1+i)^n-1}
```

For a zero periodic rate:

```math
C=\frac{FV}{n}
```

### Rate Conventions

The annual compound growth function uses an annual
effective rate. The monthly contribution functions use
a nominal annual rate divided into twelve monthly periods.

These conventions produce different effective annual
growth rates and should not be treated as interchangeable.

The public Python functions accept annual rates expressed
as percentages.

## Project Architecture

```text
finance-calculator/
├── main.py
├── calculator.py
├── history.py
├── visualization.py
├── tests/
│   └── test_calculator.py
├── .gitignore
└── README.md
```

| Module | Responsibility |
|---|---|
| calculator.py | Financial mathematical calculations |
| main.py | Command-line interface and application control |
| history.py | Local calculation history |
| visualization.py | Growth and scenario comparison charts |
| tests/ | Automated mathematical validation |

The mathematical functions are separated from application
interaction, history storage, and graphical visualization.

## Python Examples

The calculation functions can be imported independently
of the command-line interface.

### Compound Growth

```python
from calculator import future_value

result = future_value(1000, 7, 10)

print(f"${result:,.2f}")
```

Expected output:

```text
$1,967.15
```

### Periodic Contributions

```python
from calculator import future_value_monthly

result = future_value_monthly(100, 7, 10)

print(f"${result:,.2f}")
```

Expected output:

```text
$17,308.48
```

These examples use hypothetical mathematical assumptions
rather than predictions of actual financial performance.

## Visualization

The application includes three visualization options:

- Compound growth line chart.
- Annual balance bar chart.
- Comparative growth-rate scenarios.

Visualizations are generated using Matplotlib.

## Automated Testing

Run the existing automated tests:

```bash
python -m pytest -q
```

The initial test suite covers:

- Annual compound growth.
- Monthly contribution accumulation.
- Financial goal calculations.

## Limitations

The current mathematical models assume constant growth
rates and fixed periodic contributions.

The application does not model:

- Market volatility or changing asset prices.
- Taxes, transaction costs, or management fees.
- Inflation.
- Uncertain future returns.
- Individual financial circumstances.

Additional validation of numerical inputs and edge cases
is planned.

The software is intended for educational financial
mathematics and computational exploration.

## Future Development

Planned extensions include:

- Comprehensive mathematical input validation.
- Consistent interest-rate conventions.
- Combined principal and contribution models.
- Inflation-adjusted calculations.
- Expanded sensitivity analysis.
- Structured data exports.
- Comprehensive automated testing.
- Continuous integration.
- Interactive web application.
- Versioned software releases.

## Related Projects

This repository represents a foundational stage of a
broader computational mathematics and quantitative
finance project collection.

[Derivatives Pricing Laboratory](https://github.com/LakshSuri/derivatives-pricing-lab)

[Interactive Derivatives Research Laboratory](https://derivatives-research-lab.streamlit.app)

[Coding Journey](https://github.com/LakshSuri/coding-journey)