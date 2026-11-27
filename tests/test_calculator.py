import math

import pytest

from calculator import (
    future_value,
    future_value_monthly,
    monthly_investment_goal,
    effective_monthly_rate,
    present_value,
    combined_future_value,
    inflation_adjusted_value,
    projection_breakdown,
    annuity_factor
)


# Original calculation behavior


def test_future_value():
    assert future_value(
        1000, 7, 10
    ) == pytest.approx(1967.151357)


def test_future_value_monthly():
    assert round(
        future_value_monthly(100, 7, 10), 2
    ) == 17308.48


def test_monthly_investment_goal():
    assert round(
        monthly_investment_goal(50000, 7, 10), 2
    ) == 288.88


# Compound growth


@pytest.mark.parametrize(
    "amount,rate,years,expected",
    [
        (1000, 0, 10, 1000),
        (1000, 10, 1, 1100),
        (1000, 10, 2, 1210),
        (1000, -10, 2, 810),
        (1000, 7, 0, 1000),
        (0, 7, 10, 0)
    ]
)
def test_compound_growth(
    amount, rate, years, expected
):
    assert future_value(
        amount, rate, years
    ) == pytest.approx(expected)


# Monthly contributions


@pytest.mark.parametrize(
    "amount,rate,years,expected",
    [
        (100, 0, 10, 12000),
        (100, 0, 1, 1200),
        (0, 7, 10, 0),
        (100, 7, 0, 0),
        (250, 0, 5, 15000)
    ]
)
def test_monthly_contributions(
    amount, rate, years, expected
):
    assert future_value_monthly(
        amount, rate, years
    ) == pytest.approx(expected)


@pytest.mark.parametrize(
    "rate",
    [-10, -2, 0, 3, 7, 12]
)
def test_goal_calculation_inverse(rate):
    target = 50000

    contribution = monthly_investment_goal(
        target, rate, 10
    )

    result = future_value_monthly(
        contribution, rate, 10
    )

    assert result == pytest.approx(target)


# Effective annual rates


@pytest.mark.parametrize(
    "rate",
    [-50, -10, 0, 5, 12, 25]
)
def test_effective_rate_conversion(rate):
    monthly_rate = effective_monthly_rate(rate)

    annual_growth = (
        1 + monthly_rate
    ) ** 12

    assert annual_growth == pytest.approx(
        1 + rate / 100
    )


# Present value


@pytest.mark.parametrize(
    "rate",
    [-20, -5, 0, 3, 7, 15]
)
def test_present_value_inverse(rate):
    principal = 1000

    accumulated = future_value(
        principal, rate, 10
    )

    discounted = present_value(
        accumulated, rate, 10
    )

    assert discounted == pytest.approx(
        principal
    )


def test_present_value_zero_years():
    assert present_value(
        5000, 7, 0
    ) == pytest.approx(5000)


# Combined principal and contribution model


def test_combined_zero_rate():
    result = combined_future_value(
        1000, 100, 0, 10
    )

    assert result == pytest.approx(13000)


def test_combined_zero_contributions():
    result = combined_future_value(
        1000, 0, 7, 10
    )

    assert result == pytest.approx(
        future_value(1000, 7, 10)
    )


def test_combined_zero_years():
    result = combined_future_value(
        1000, 100, 7, 0
    )

    assert result == pytest.approx(1000)


@pytest.mark.parametrize(
    "rate",
    [-10, 0, 5, 10, 20]
)
def test_combined_against_monthly_iteration(rate):
    starting_amount = 1000
    contribution = 100
    years = 10

    monthly_rate = effective_monthly_rate(rate)

    balance = starting_amount

    for _ in range(years * 12):
        balance *= 1 + monthly_rate
        balance += contribution

    analytical = combined_future_value(
        starting_amount,
        contribution,
        rate,
        years
    )

    assert analytical == pytest.approx(
        balance, rel=1e-10
    )


# Inflation adjustment


def test_inflation_adjustment():
    result = inflation_adjusted_value(
        1210, 10, 2
    )

    assert result == pytest.approx(1000)


def test_zero_inflation():
    assert inflation_adjusted_value(
        1000, 0, 10
    ) == pytest.approx(1000)


def test_negative_inflation():
    result = inflation_adjusted_value(
        1000, -10, 2
    )

    assert result == pytest.approx(
        1000 / 0.9 ** 2
    )


# Projection accounting


def test_projection_breakdown():
    result = projection_breakdown(
        1000, 100, 7, 10, 2
    )

    assert result["starting_amount"] == 1000
    assert result["total_contributions"] == 12000
    assert result["total_principal"] == 13000

    assert (
        result["total_principal"]
        + result["nominal_growth"]
    ) == pytest.approx(
        result["nominal_future_value"]
    )

    assert result[
        "inflation_adjusted_value"
    ] == pytest.approx(
        result["nominal_future_value"] / 1.02 ** 10
    )


def test_negative_growth_breakdown():
    result = projection_breakdown(
        1000, 0, -10, 5
    )

    assert result["nominal_growth"] < 0

    assert result["nominal_future_value"] > 0


# Numerical stability


@pytest.mark.parametrize(
    "rate",
    [-1e-12, 0, 1e-12]
)
def test_near_zero_periodic_rate(rate):
    result = annuity_factor(rate, 120)

    assert result == pytest.approx(
        120, rel=1e-9
    )


def test_near_zero_annual_rate():
    result = combined_future_value(
        1000, 100, 1e-12, 10
    )

    assert result == pytest.approx(
        13000, rel=1e-9
    )


def test_zero_period_annuity():
    assert annuity_factor(0.01, 0) == 0


# Input validation


@pytest.mark.parametrize(
    "amount",
    [
        -100,
        math.nan,
        math.inf,
        -math.inf,
        None,
        "invalid",
        True
    ]
)
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        future_value(amount, 7, 10)


@pytest.mark.parametrize(
    "rate",
    [
        -100,
        -150,
        math.nan,
        math.inf,
        -math.inf,
        None
    ]
)
def test_invalid_annual_rate(rate):
    with pytest.raises(ValueError):
        future_value(1000, rate, 10)


@pytest.mark.parametrize(
    "years",
    [-1, 1.5, math.nan, math.inf, True, None]
)
def test_invalid_years(years):
    with pytest.raises(ValueError):
        future_value(1000, 7, years)


def test_invalid_monthly_rate():
    with pytest.raises(ValueError):
        future_value_monthly(
            100, -1200, 10
        )


def test_invalid_goal_duration():
    with pytest.raises(ValueError):
        monthly_investment_goal(
            50000, 7, 0
        )


def test_negative_monthly_contribution():
    with pytest.raises(ValueError):
        combined_future_value(
            1000, -100, 7, 10
        )


def test_invalid_inflation_rate():
    with pytest.raises(ValueError):
        inflation_adjusted_value(
            1000, -100, 10
        )


def test_growth_overflow():
    with pytest.raises(ValueError):
        future_value(
            1000, 1000, 10000
        )