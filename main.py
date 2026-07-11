import calculator


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
    print("Finance Calculator")
    print("------------------")
    print("1. Calculate future investment value")
    print("2. Calculate value with monthly contributions")
    print("3. Calculate monthly investment needed to reach a goal")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        amount = get_number("Starting investment amount: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.future_value(amount, return_rate, years)

        print()
        print(f"After {years} years, your investment could be worth ${result:,.2f}")

    elif choice == "2":
        monthly_amount = get_number("Monthly contribution: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.future_value_monthly(monthly_amount, return_rate, years)

        print()
        print(f"After {years} years, your investment could be worth ${result:,.2f}")

    elif choice == "3":
        goal_amount = get_number("Goal amount: ")
        return_rate = get_number("Expected yearly return (%): ")
        years = get_years("Number of years: ")

        result = calculator.monthly_investment_goal(goal_amount, return_rate, years)

        print()
        print(f"You would need to invest about ${result:,.2f} each month.")

    elif choice == "4":
        print("Thanks for using the Finance Calculator!")
        break

    else:
        print("Please choose a valid option.")
        continue

    if not continue_calculating():
        print("Thanks for using the Finance Calculator!")
        break