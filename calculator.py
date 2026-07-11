def future_value(amount, return_rate, years):
    growth = (1 + return_rate / 100) ** years
    return amount * growth


def future_value_monthly(monthly_amount, return_rate, years):
    monthly_rate = (return_rate / 100) / 12
    months = years * 12

    if monthly_rate == 0:
        return monthly_amount * months

    value = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    return value


def monthly_investment_goal(goal_amount, return_rate, years):
    monthly_rate = (return_rate / 100) / 12
    months = years * 12

    if monthly_rate == 0:
        return goal_amount / months

    monthly_amount = goal_amount * monthly_rate / (((1 + monthly_rate) ** months) - 1)

    return monthly_amount