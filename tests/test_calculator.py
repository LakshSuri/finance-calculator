import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import calculator


def test_future_value():
    result = calculator.future_value(1000, 7, 10)
    assert round(result, 2) == 1967.15


def test_future_value_monthly():
    result = calculator.future_value_monthly(100, 7, 10)
    assert round(result, 2) == 17308.48


def test_monthly_investment_goal():
    result = calculator.monthly_investment_goal(50000, 7, 10)
    assert round(result, 2) == 288.88
