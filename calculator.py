import math


def validate_number(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number.")

    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(
            f"{name} must be a finite number."
        ) from None

    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")

    return value


def validate_amount(value, name):
    value = validate_number(value, name)

    if value < 0:
        raise ValueError(f"{name} cannot be negative.")

    return value


def validate_years(years, minimum=0):
    years = validate_number(years, "Years")

    if not years.is_integer():
        raise ValueError("Years must be a whole number.")

    if years < minimum:
        raise ValueError(
            f"Years must be at least {minimum}."
        )

    return int(years)


def validate_rate(return_rate, minimum=-100):
    return_rate = validate_number(
        return_rate,
        "Annual rate"
    )

    if return_rate <= minimum:
        raise ValueError(
            f"Annual rate must be greater than {minimum}%."
        )

    return return_rate / 100


def validate_result(value):
    if not math.isfinite(value):
        raise ValueError(
            "Calculated value exceeds numerical limits."
        )

    return value


def growth_factor(rate, periods):
    try:
        return validate_result(
            math.exp(periods * math.log1p(rate))
        )
    except OverflowError:
        raise ValueError(
            "Growth exceeds numerical limits."
        ) from None


def annuity_factor(periodic_rate, periods):
    if periods == 0:
        return 0.0

    if periodic_rate == 0:
        return float(periods)

    try:
        growth = math.expm1(
            periods * math.log1p(periodic_rate)
        )

        return validate_result(
            growth / periodic_rate
        )

    except OverflowError:
        raise ValueError(
            "Annuity exceeds numerical limits."
        ) from None


def future_value(amount, return_rate, years):
    amount = validate_amount(
        amount,
        "Starting amount"
    )

    rate = validate_rate(return_rate)
    years = validate_years(years)

    return validate_result(
        amount * growth_factor(rate, years)
    )


def future_value_monthly(
    monthly_amount,
    return_rate,
    years
):
    monthly_amount = validate_amount(
        monthly_amount,
        "Monthly contribution"
    )

    annual_rate = validate_rate(
        return_rate,
        minimum=-1200
    )

    years = validate_years(years)

    monthly_rate = annual_rate / 12
    months = years * 12

    return validate_result(
        monthly_amount * annuity_factor(
            monthly_rate,
            months
        )
    )


def monthly_investment_goal(
    goal_amount,
    return_rate,
    years
):
    goal_amount = validate_amount(
        goal_amount,
        "Target amount"
    )

    annual_rate = validate_rate(
        return_rate,
        minimum=-1200
    )

    years = validate_years(
        years,
        minimum=1
    )

    monthly_rate = annual_rate / 12
    months = years * 12

    factor = annuity_factor(
        monthly_rate,
        months
    )

    return validate_result(
        goal_amount / factor
    )


def effective_monthly_rate(annual_rate):
    rate = validate_rate(annual_rate)

    return math.expm1(
        math.log1p(rate) / 12
    )


def present_value(
    future_amount,
    discount_rate,
    years
):
    future_amount = validate_amount(
        future_amount,
        "Future amount"
    )

    rate = validate_rate(discount_rate)
    years = validate_years(years)

    try:
        discount_factor = math.exp(
            -years * math.log1p(rate)
        )
    except OverflowError:
        raise ValueError(
            "Discount factor exceeds numerical limits."
        ) from None

    return validate_result(
        future_amount * discount_factor
    )


def combined_future_value(
    starting_amount,
    monthly_amount,
    annual_rate,
    years
):
    starting_amount = validate_amount(
        starting_amount,
        "Starting amount"
    )

    monthly_amount = validate_amount(
        monthly_amount,
        "Monthly contribution"
    )

    years = validate_years(years)

    monthly_rate = effective_monthly_rate(
        annual_rate
    )

    initial_growth = future_value(
        starting_amount,
        annual_rate,
        years
    )

    contribution_growth = monthly_amount * annuity_factor(
        monthly_rate,
        years * 12
    )

    return validate_result(
        initial_growth + contribution_growth
    )


def inflation_adjusted_value(
    nominal_amount,
    inflation_rate,
    years
):
    return present_value(
        nominal_amount,
        inflation_rate,
        years
    )


def projection_breakdown(
    starting_amount,
    monthly_amount,
    annual_rate,
    years,
    inflation_rate=0
):
    starting_amount = validate_amount(
        starting_amount,
        "Starting amount"
    )

    monthly_amount = validate_amount(
        monthly_amount,
        "Monthly contribution"
    )

    years = validate_years(years)

    final_value = combined_future_value(
        starting_amount,
        monthly_amount,
        annual_rate,
        years
    )

    contributions = validate_result(
        monthly_amount * years * 12
    )

    total_principal = validate_result(
        starting_amount + contributions
    )

    real_value = inflation_adjusted_value(
        final_value,
        inflation_rate,
        years
    )

    return {
        "starting_amount": starting_amount,
        "total_contributions": contributions,
        "total_principal": total_principal,
        "nominal_future_value": final_value,
        "nominal_growth": final_value - total_principal,
        "inflation_adjusted_value": real_value,
        "annual_rate": annual_rate,
        "inflation_rate": inflation_rate,
        "years": years
    }