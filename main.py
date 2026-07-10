import calculator

print("Finance Calculator")
print(" ")
print("1. Calculate future investment value")
print("2. Calculate value with monthly contributions")

choice = input("Choose an option: ")

if choice == "1":
    amount = float(input("Starting investment amount: "))
    return_rate = float(input("Expected yearly return (%): "))
    years = int(input("Number of years: "))

    result = calculator.future_value(amount, return_rate, years)

    print()
    print(f"After {years} years, your investment could be worth ${result:,.2f}")

elif choice == "2":
    monthly_amount = float(input("Monthly contribution: "))
    return_rate = float(input("Expected yearly return (%): "))
    years = int(input("Number of years: "))

    result = calculator.future_value_monthly(monthly_amount, return_rate, years)

    print()
    print(f"After {years} years, your investment could be worth ${result:,.2f}")

else:
    print("Please choose a valid option.")
