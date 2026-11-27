import math

import calculator
import history
import visualization


def get_number(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt))

            if not math.isfinite(value):
                raise ValueError("Enter a finite number.")

            if minimum is not None and value < minimum:
                raise ValueError(
                    f"Enter a value of at least {minimum}."
                )

            if maximum is not None and value > maximum:
                raise ValueError(
                    f"Enter a value no greater than {maximum}."
                )

            return value

        except ValueError as error:
            print(f"Invalid input: {error}")


def get_years():
    while True:
        try:
            years = int(input("Number of years: "))

            if not 1 <= years <= 100:
                raise ValueError

            return years

        except ValueError:
            print("Enter a whole number between 1 and 100.")


def get_amount(prompt):
    return get_number(prompt, minimum=0)


def get_rate(prompt):
    return get_number(
        prompt,
        minimum=-99,
        maximum=100
    )


def currency(value):
    return f"${value:,.2f}"


def print_heading(title):
    print()
    print("=" * 52)
    print(title.center(52))
    print("=" * 52)


def display_result(label, value):
    print(f"{label:<30} {currency(value):>20}")


def record_calculation(title, inputs, results):
    lines = [title, "-" * len(title)]

    for label, value in inputs.items():
        lines.append(f"{label}: {value}")

    for label, value in results.items():
        lines.append(f"{label}: {value}")

    history.save_history("\n".join(lines))


def investment_growth():
    print_heading("Compound Growth Analysis")

    amount = get_amount("Starting amount: $")
    rate = get_rate("Effective annual growth rate (%): ")
    years = get_years()

    result = calculator.future_value(
        amount, rate, years
    )

    display_result("Initial principal", amount)
    display_result("Calculated future value", result)
    display_result("Nominal growth", result - amount)

    record_calculation(
        "Compound Growth Analysis",
        {
            "Initial principal": currency(amount),
            "Effective annual rate": f"{rate}%",
            "Years": years
        },
        {"Future value": currency(result)}
    )


def monthly_contributions():
    print_heading("Monthly Contribution Analysis")

    amount = get_amount("Monthly contribution: $")
    rate = get_rate("Nominal annual rate (%): ")
    years = get_years()

    result = calculator.future_value_monthly(
        amount, rate, years
    )

    principal = amount * years * 12

    display_result("Total contributions", principal)
    display_result("Calculated future value", result)
    display_result("Nominal growth", result - principal)

    record_calculation(
        "Monthly Contribution Analysis",
        {
            "Monthly contribution": currency(amount),
            "Nominal annual rate": f"{rate}%",
            "Years": years
        },
        {"Future value": currency(result)}
    )


def financial_goal():
    print_heading("Financial Goal Calculation")

    target = get_amount("Hypothetical target: $")
    rate = get_rate("Nominal annual rate (%): ")
    years = get_years()

    result = calculator.monthly_investment_goal(
        target, rate, years
    )

    display_result("Hypothetical target", target)
    display_result("Calculated monthly amount", result)

    record_calculation(
        "Financial Goal Calculation",
        {
            "Target": currency(target),
            "Nominal annual rate": f"{rate}%",
            "Years": years
        },
        {"Monthly amount": currency(result)}
    )


def combined_projection():
    print_heading("Combined Growth Projection")

    starting_amount = get_amount("Starting amount: $")
    monthly_amount = get_amount("Monthly contribution: $")
    rate = get_rate("Effective annual growth rate (%): ")
    inflation = get_rate("Annual inflation rate (%): ")
    years = get_years()

    result = calculator.projection_breakdown(
        starting_amount,
        monthly_amount,
        rate,
        years,
        inflation
    )

    print()

    display_result(
        "Starting principal",
        result["starting_amount"]
    )

    display_result(
        "Total contributions",
        result["total_contributions"]
    )

    display_result(
        "Total principal",
        result["total_principal"]
    )

    display_result(
        "Nominal growth",
        result["nominal_growth"]
    )

    display_result(
        "Nominal future value",
        result["nominal_future_value"]
    )

    display_result(
        "Inflation-adjusted value",
        result["inflation_adjusted_value"]
    )

    record_calculation(
        "Combined Growth Projection",
        {
            "Starting amount": currency(starting_amount),
            "Monthly contribution": currency(monthly_amount),
            "Effective annual rate": f"{rate}%",
            "Inflation rate": f"{inflation}%",
            "Years": years
        },
        {
            "Nominal future value": currency(
                result["nominal_future_value"]
            ),
            "Inflation-adjusted value": currency(
                result["inflation_adjusted_value"]
            )
        }
    )


def present_value_analysis():
    print_heading("Present Value Analysis")

    amount = get_amount("Future amount: $")
    rate = get_rate("Effective annual discount rate (%): ")
    years = get_years()

    result = calculator.present_value(
        amount, rate, years
    )

    display_result("Future amount", amount)
    display_result("Calculated present value", result)

    record_calculation(
        "Present Value Analysis",
        {
            "Future amount": currency(amount),
            "Discount rate": f"{rate}%",
            "Years": years
        },
        {"Present value": currency(result)}
    )


def inflation_analysis():
    print_heading("Purchasing Power Analysis")

    amount = get_amount("Nominal future amount: $")
    inflation = get_rate("Annual inflation rate (%): ")
    years = get_years()

    result = calculator.inflation_adjusted_value(
        amount, inflation, years
    )

    display_result("Nominal future amount", amount)
    display_result("Inflation-adjusted value", result)
    display_result("Purchasing power change", result - amount)

    record_calculation(
        "Purchasing Power Analysis",
        {
            "Nominal amount": currency(amount),
            "Inflation rate": f"{inflation}%",
            "Years": years
        },
        {"Inflation-adjusted value": currency(result)}
    )


def rate_conversion():
    print_heading("Interest Rate Conversion")

    rate = get_rate("Effective annual rate (%): ")

    monthly_rate = calculator.effective_monthly_rate(
        rate
    )

    print(f"Effective annual rate: {rate:.6f}%")
    print(f"Equivalent monthly rate: {monthly_rate * 100:.6f}%")
    print(f"Equivalent nominal annual rate: {monthly_rate * 1200:.6f}%")


def visualization_menu():
    print_heading("Financial Visualizations")

    print("[1] Compound Growth Line Chart")
    print("[2] Annual Balance Bar Chart")
    print("[3] Growth Rate Scenario Comparison")
    print("[4] Combined Growth Projection")
    print("[5] Contribution and Growth Breakdown")
    print("[6] Purchasing Power Sensitivity")
    print("[7] Return to Main Menu")

    choice = input("\nSelect visualization: ").strip()

    if choice == "7":
        return

    if choice not in ("1", "2", "3", "4", "5", "6"):
        print("Invalid visualization selection.")
        return

    amount = get_amount("Starting amount: $")

    if choice in ("1", "2"):
        rate = get_rate(
            "Effective annual growth rate (%): "
        )

        years = get_years()

        if choice == "1":
            visualization.create_growth_chart(
                amount, rate, years
            )

        else:
            visualization.create_bar_chart(
                amount, rate, years
            )

    elif choice == "3":
        years = get_years()

        visualization.create_return_comparison_chart(
            amount, years
        )

    elif choice in ("4", "5", "6"):
        monthly_amount = get_amount(
            "Monthly contribution: $"
        )

        rate = get_rate(
            "Effective annual growth rate (%): "
        )

        years = get_years()

        if choice == "4":
            inflation = get_rate(
                "Annual inflation rate (%): "
            )

            visualization.create_combined_projection_chart(
                amount,
                monthly_amount,
                rate,
                years,
                inflation
            )

        elif choice == "5":
            visualization.create_contribution_breakdown_chart(
                amount,
                monthly_amount,
                rate,
                years
            )

        elif choice == "6":
            visualization.create_inflation_comparison_chart(
                amount,
                monthly_amount,
                rate,
                years
            )


def main():
    operations = {
        "1": investment_growth,
        "2": monthly_contributions,
        "3": financial_goal,
        "4": combined_projection,
        "5": present_value_analysis,
        "6": inflation_analysis,
        "7": rate_conversion,
        "8": history.view_history,
        "9": visualization_menu
    }

    print(
        "\nEducational financial mathematics laboratory."
        "\nAll calculations use hypothetical assumptions."
    )

    while True:
        print_heading("FINANCE CALCULATOR")

        print("[1] Compound Growth Analysis")
        print("[2] Monthly Contribution Analysis")
        print("[3] Financial Goal Calculation")
        print("[4] Combined Growth Projection")
        print("[5] Present Value Analysis")
        print("[6] Purchasing Power Analysis")
        print("[7] Interest Rate Conversion")
        print("[8] Calculation History")
        print("[9] Financial Visualizations")
        print("[10] Exit")

        try:
            choice = input("\nSelect operation: ").strip()

            if choice == "10":
                print("\nFinance Calculator closed.")
                break

            operation = operations.get(choice)

            if operation is None:
                print("Select a valid operation.")
                continue

            operation()

            input("\nPress Enter to return to the menu.")

        except (ValueError, OverflowError, OSError) as error:
            print(f"\nOperation could not be completed: {error}")

        except (KeyboardInterrupt, EOFError):
            print("\nFinance Calculator closed.")
            break


if __name__ == "__main__":
    main()