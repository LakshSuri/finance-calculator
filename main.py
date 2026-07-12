import calculator
import history
import visualization


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_years(prompt):
    while True:
        try:
            years = int(input(prompt))

            if years > 0:
                return years

            print("Please enter a number greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def continue_calculating():
    while True:
        answer = input("\nWould you like to make another calculation? (y/n): ")

        if answer.lower() == "y":
            return True

        elif answer.lower() == "n":
            return False

        else:
            print("Please enter y or n.")


while True:
    print()
    print("================================")
    print("       Finance Calculator")
    print("================================")
    print()
    print("[1] Investment Growth Projection")
    print("[2] Monthly Contribution Planner")
    print("[3] Financial Goal Planner")
    print("[4] View Calculation History")
    print("[5] Investment Visualizations")
    print("[6] Exit Program")

    choice = input("\nChoose an option: ")

    if choice == "1":
        amount = get_number("Starting investment amount: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.future_value(amount, return_rate, years)

        history.save_history(
            f"Investment Growth Projection\n"
            f"Starting amount: ${amount:,.2f}\n"
            f"Return: {return_rate}%\n"
            f"Years: {years}\n"
            f"Result: ${result:,.2f}\n"
        )

        print()
        print(f"After {years} years, your investment could be worth ${result:,.2f}")


    elif choice == "2":
        monthly_amount = get_number("Monthly contribution: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.future_value_monthly(
            monthly_amount,
            return_rate,
            years
        )

        history.save_history(
            f"Monthly Contribution Planner\n"
            f"Monthly contribution: ${monthly_amount:,.2f}\n"
            f"Return: {return_rate}%\n"
            f"Years: {years}\n"
            f"Result: ${result:,.2f}\n"
        )

        print()
        print(f"After {years} years, your investment could be worth ${result:,.2f}")


    elif choice == "3":
        goal_amount = get_number("Goal amount: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.monthly_investment_goal(
            goal_amount,
            return_rate,
            years
        )

        history.save_history(
            f"Financial Goal Planner\n"
            f"Goal amount: ${goal_amount:,.2f}\n"
            f"Return: {return_rate}%\n"
            f"Years: {years}\n"
            f"Monthly investment needed: ${result:,.2f}\n"
        )

        print()
        print(f"You would need to invest about ${result:,.2f} each month.")


    elif choice == "4":
        history.view_history()


    elif choice == "5":
        print()
        print("Investment Visualizations")
        print("-------------------------")
        print("[1] Growth Line Chart")
        print("[2] Yearly Growth Bar Chart")
        print("[3] Return Rate Comparison")

        chart_choice = input("\nChoose visualization: ")

        if chart_choice == "1":
            amount = get_number("Starting investment amount: ")
            return_rate = get_number("Expected yearly return (%): ")
            years = get_years("Number of years: ")

            visualization.create_growth_chart(
                amount,
                return_rate,
                years
            )

        elif chart_choice == "2":
            amount = get_number("Starting investment amount: ")
            return_rate = get_number("Expected yearly return (%): ")
            years = get_years("Number of years: ")

            visualization.create_bar_chart(
                amount,
                return_rate,
                years
            )

        elif chart_choice == "3":
            amount = get_number("Starting investment amount: ")
            years = get_years("Number of years: ")

            visualization.create_return_comparison_chart(
                amount,
                years
            )

        else:
            print("Invalid visualization choice.")


    elif choice == "6":
        print("Thanks for using the Finance Calculator!")
        break


    else:
        print("Please choose a valid option.")


    if choice != "6":
        if not continue_calculating():
            print("Thanks for using the Finance Calculator!")
            break