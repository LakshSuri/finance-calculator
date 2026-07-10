print("Finance Calculator")
print(" ")
print("1. Calculate future investment value")
print("2. Calculate value with monthly contributions")

choice = input("Choose an option: ")

if choice == "1":
    amount = float(input("Starting investment amount: "))
    return_rate = float(input("Expected yearly return (%): "))
    years = int(input("Number of years: "))

    growth = (1 + return_rate / 100) ** years
    future_amount = amount * growth

    print()
    print(f"After {years} years, your investment could be worth ${future_amount:,.2f}")

elif choice == "2":
    monthly_amount = float(input("Monthly contribution: "))
    return_rate = float(input("Expected yearly return (%): "))
    years = int(input("Number of years: "))

    monthly_rate = (return_rate / 100) / 12
    months = years * 12

    future_amount = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate)

    print()
    print(f"After {years} years, your investment could be worth ${future_amount:,.2f}")

else:
    print("Please choose a valid option.")