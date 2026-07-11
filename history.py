HISTORY_FILE = "calculation_history.txt"


def save_history(calculation):
    # Saves a completed calculation to a history file
    with open(HISTORY_FILE, "a") as file:
        file.write(calculation + "\n")


def view_history():
    # Displays previous calculations
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