import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import date, datetime
import matplotlib.pyplot as plt
from pathlib import Path

WORKOUT_FILE = Path("workouts.csv")

# ---------- Helpers ----------
def ensure_csv():
    if not WORKOUT_FILE.exists():
        with open(WORKOUT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "day", "exercise", "weight", "reps"])

def append_row(day, exercise, weight, reps):
    with open(WORKOUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([str(date.today()), day, exercise, weight, reps])

def read_rows():
    ensure_csv()
    with open(WORKOUT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = [row for row in reader][1:]  # skip header
    return rows

# ---------- GUI Class ----------
class GymTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Tracker")
        self.geometry("600x450")
        self.configure(bg="#f2f2f2")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self.create_log_tab()
        self.create_view_tab()
        self.create_chart_tab()

    # --- Tab 1: Log workout ---
    def create_log_tab(self):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text="Log Workout")

        ttk.Label(frame, text="Workout Day:").grid(row=0, column=0, padx=8, pady=5)
        self.day_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.day_var).grid(row=0, column=1, padx=8)

        ttk.Label(frame, text="Exercise:").grid(row=1, column=0, padx=8, pady=5)
        self.exercise_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.exercise_var).grid(row=1, column=1, padx=8)

        ttk.Label(frame, text="Weight (lbs):").grid(row=2, column=0, padx=8, pady=5)
        self.weight_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.weight_var).grid(row=2, column=1, padx=8)

        ttk.Label(frame, text="Reps:").grid(row=3, column=0, padx=8, pady=5)
        self.reps_var = tk.IntVar()
        ttk.Entry(frame, textvariable=self.reps_var).grid(row=3, column=1, padx=8)

        ttk.Button(frame, text="Save Workout", command=self.save_workout).grid(
            row=4, column=0, columnspan=2, pady=12
        )

    def save_workout(self):
        day = self.day_var.get().title()
        exercise = self.exercise_var.get().title()
        try:
            weight = float(self.weight_var.get())
            reps = int(self.reps_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weight and reps.")
            return

        append_row(day, exercise, weight, reps)
        messagebox.showinfo("Saved", f"Logged {exercise}: {weight} lbs × {reps} reps")
        self.day_var.set("")
        self.exercise_var.set("")
        self.weight_var.set(0)
        self.reps_var.set(0)
        self.refresh_table()

    # --- Tab 2: View logs ---
    def create_view_tab(self):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text="View Logs")

        columns = ("date", "day", "exercise", "weight", "reps")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        self.refresh_table_btn = ttk.Button(frame, text="Refresh", command=self.refresh_table)
        self.refresh_table_btn.pack(pady=4)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in read_rows():
            self.tree.insert("", "end", values=row)

    # --- Tab 3: Progress chart ---
    def create_chart_tab(self):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text="Progress Chart")

        ttk.Label(frame, text="Exercise name:").pack(pady=6)
        self.chart_exercise = tk.StringVar()
        ttk.Entry(frame, textvariable=self.chart_exercise).pack(pady=4)

        ttk.Button(frame, text="Show Chart", command=self.show_chart).pack(pady=10)

    def show_chart(self):
        name = self.chart_exercise.get().strip().title()
        if not name:
            messagebox.showwarning("Input Needed", "Enter an exercise name.")
            return

        rows = read_rows()
        dates, weights, reps = [], [], []
        for row in rows:
            try:
                d, _, ex, w, r = row
                if ex.strip().title() == name:
                    dates.append(datetime.strptime(d, "%Y-%m-%d"))
                    weights.append(float(w))
                    reps.append(int(r))
            except Exception:
                continue

        if not dates:
            messagebox.showinfo("No Data", f"No logs found for {name}.")
            return

        combined = sorted(zip(dates, weights, reps), key=lambda x: x[0])
        dates, weights, reps = zip(*combined)

        fig, ax1 = plt.subplots(figsize=(7, 4))
        ax1.plot(dates, weights, "o-", label="Weight (lbs)")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Weight (lbs)")
        ax2 = ax1.twinx()
        ax2.plot(dates, reps, "s--", color="orange", label="Reps")
        ax2.set_ylabel("Reps")

        lines, labels = [], []
        for ax in [ax1, ax2]:
            lns, lbls = ax.get_legend_handles_labels()
            lines += lns
            labels += lbls
        ax1.legend(lines, labels, loc="best")

        plt.title(f"{name} Progress")
        plt.tight_layout()
        plt.show()


# ---------- Run ----------
if __name__ == "__main__":
    ensure_csv()
    app = GymTrackerGUI()
    app.mainloop()
