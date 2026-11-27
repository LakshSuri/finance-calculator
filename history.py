HISTORY_FILE = "calculation_history.txt"


def save_history(calculation):
    with open(HISTORY_FILE, "a") as file:
        file.write(calculation + "\n")


def view_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = file.read()

            if history:
                print("\nCalculation History:")
                print("--------------------")
                print(history)
            else:
                print("\nNo calculations found.")

    except FileNotFoundError:
        print("\nNo calculations found.")
