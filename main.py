import json
import csv
from datetime import date

PROGRAM_FILE = "program.json"
WORKOUT_FILE = "workouts.csv"

def load_program():
    try:
        with open(PROGRAM_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_program(program):
    with open(PROGRAM_FILE, 'w') as f:
        json.dump(program, f, indent=2)


def remove_exercise_from_program(program: dict) -> None:
    """Interactively remove an exercise from the saved program."""
    if not program:
        print("No program found. Add some exercises first.\n")
        return

    # List days
    days = sorted(program.keys())
    print("\n-- Program Days --")
    for i, day in enumerate(days, start=1):
        print(f"{i}. {day}")

    try:
        day_idx = int(input("Select a day number to edit: ").strip())
    except ValueError:
        print("Invalid input.\n")
        return

    if not (1 <= day_idx <= len(days)):
        print("Day number out of range.\n")
        return

    day = days[day_idx - 1]
    exercises = program.get(day, [])
    if not exercises:
        print(f"No exercises listed for {day}.\n")
        return

    # List exercises for chosen day
    print(f"\n-- {day} Exercises --")
    for j, ex in enumerate(exercises, start=1):
        print(f"{j}. {ex}")

    try:
        ex_idx = int(input("Select an exercise number to remove: ").strip())
    except ValueError:
        print("Invalid input.\n")
        return

    if not (1 <= ex_idx <= len(exercises)):
        print("Exercise number out of range.\n")
        return

    removed = exercises.pop(ex_idx - 1)
    print(f"🗑️ Removed '{removed}' from {day}.")

    # If that day is now empty, offer to delete the day entirely
    if len(exercises) == 0:
        choice = input(f"'{day}' has no exercises left. Remove this day as well? (y/n): ").strip().lower()
        if choice == "y":
            del program[day]
            print(f"🗑️ Removed day '{day}'.")

    save_program(program)
    print()


def add_day_with_exercises(program: dict) -> None:
    """Create or update a day with multiple exercises in one go."""
    day = input("Day name (e.g., Push, Pull, Legs, Upper, Lower): ").strip().title()
    raw = input("Enter exercises separated by commas:\n> ").strip()

    # Split, clean, and title-case each exercise
    items = [ex.strip().title() for ex in raw.split(",") if ex.strip()]

    if not items:
        print("No exercises provided.\n")
        return

    # Create day if needed
    program.setdefault(day, [])

    # Add without duplicates
    added = 0
    for ex in items:
        if ex not in program[day]:
            program[day].append(ex)
            added += 1

    if added == 0:
        print(f"No new exercises added to {day} (all were duplicates).\n")
    else:
        print(f"✅ Added {added} exercise(s) to {day}.\n")

    save_program(program)

def log_workout():
    day = input("What are you hitting today? (e.g, Push, Pull, Legs): ").title()
    exercise = input("What exercise did you just complete?: ").title()
    weight = float(input("Weight (lbs): "))
    reps = int(input("Reps: "))

    with open(WORKOUT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(date.today()), day, exercise, weight, reps])
    print(f"✅ Workout has been logged!\n")


def view_log():
    try:
        with open(WORKOUT_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = [row for row in reader if row]
    except FileNotFoundError:
        print("No workouts logged yet.\n")
        return

    if not rows:
        print("No workouts logged yet.\n")
        return

    expected_header = ["date", "day", "exercise", "weight", "reps"]
    has_header = len(rows[0]) >= 5 and [c.strip().lower() for c in rows[0][:5]] == expected_header
    start = 1 if has_header else 0

    if len(rows) == start:
        print("No workouts logged yet.\n")
        return

    print("\n---- Workout Log ----")
    for row in rows[start:]:
        # Defensive formatting in case a row is malformed
        date_str = row[0] if len(row) > 0 else "?"
        day = row[1] if len(row) > 1 else "?"
        exercise = row[2] if len(row) > 2 else "?"
        weight = row[3] if len(row) > 3 else "?"
        reps = row[4] if len(row) > 4 else "?"
        print(f"{date_str} | {day:<6} | {exercise:<20} | {weight:>6} lbs x {reps}")
    print()

def remove_log_entry():
    """ Show all logged workouts and let the user delete one"""
    try:
        with open(WORKOUT_FILE, 'r', newline='') as f:
            reader = list(csv.reader(f))
    except FileNotFoundError:
        print("No workouts have been logged yet\n")
        return

    if not reader:
        print("No data to remove.\n")
        return

    # Display all rows with index numbers
    print("\n---- Logged Workouts ----")
    for i, row in enumerate(reader, start=1):
        print(f"{i}. {row}")

    try:
        idx = int(input("\nEnter the number of the entry to delete: "))
    except ValueError:
        print("Invalid input.\n")
        return

    if 1 <= idx <= len(reader):
        removed = reader.pop(idx-1)
        print(f"🗑️ Removed entry: {removed}\n")

        # Rewrite the CSV file with the remaining rows
        with open(WORKOUT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(reader)
    else:
        print("Index out of range.\n")


def main():
    program = load_program()

    while True:
        print("---- Gym Tracker ----")
        print("1. View Program")
        print("2. Add Exercise(s)")
        print("3. Log Workout")
        print("4. View Log")
        print("5. Remove Log Entry")
        print("6. Remove Exercise")
        print("7. Exit")
        choice = input("> ")

        if choice == "1":
            print(json.dumps(program, indent=2))
        elif choice == "2":
            add_day_with_exercises(program)
        elif choice == "3":
            log_workout()
        elif choice == "4":
            view_log()
        elif choice == "5":
            remove_log_entry()
        elif choice == "6":
            remove_exercise_from_program(program)
        elif choice == "7":
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
