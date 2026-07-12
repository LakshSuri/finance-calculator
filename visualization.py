import matplotlib.pyplot as plt


def calculate_yearly_growth(starting_amount, return_rate, years):
    values = []
    yearly_values = []

    amount = starting_amount

    for year in range(1, years + 1):
        amount = amount * (1 + return_rate / 100)

        yearly_values.append(year)
        values.append(amount)

    return yearly_values, values


def create_growth_chart(starting_amount, return_rate, years):
    yearly_values, values = calculate_yearly_growth(
        starting_amount,
        return_rate,
        years
    )

    plt.plot(yearly_values, values, marker="o")

    plt.title("Investment Growth Over Time")
    plt.xlabel("Years")
    plt.ylabel("Investment Value ($)")

    plt.grid(True)
    plt.show()


def create_bar_chart(starting_amount, return_rate, years):
    yearly_values, values = calculate_yearly_growth(
        starting_amount,
        return_rate,
        years
    )

    plt.bar(yearly_values, values)

    plt.title("Yearly Investment Growth")
    plt.xlabel("Years")
    plt.ylabel("Investment Value ($)")

    plt.show()


def create_return_comparison_chart(starting_amount, years):
    rates = [5, 7, 10]

    for rate in rates:
        yearly_values, values = calculate_yearly_growth(
            starting_amount,
            rate,
            years
        )

        plt.plot(
            yearly_values,
            values,
            marker="o",
            label=f"{rate}% Return"
        )

    plt.title("Investment Return Comparison")
    plt.xlabel("Years")
    plt.ylabel("Investment Value ($)")

    plt.legend()
    plt.grid(True)

    plt.show()