def future_value(amount, return_rate, years):
    growth = (1 + return_rate / 100) ** years
    return amount * growth


def future_value_monthly(monthly_amount, return_rate, years):
    monthly_rate = (return_rate / 100) / 12
    months = years * 12

    value = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    return value
