# 🏋️‍♂️ Gym Progression Tracker
A Python-based workout tracker for logging and visualizing strength training progress.  
Features a simple console interface and optional Tkinter-based visualization.

---

## About The Project

The **Gym Progression Tracker** helps users log their workouts, review progress, and visualize strength improvements.  
It offers a menu-based console interface and an optional Tkinter GUI for future extension.  
Data is stored locally using **CSV** and **JSON**, ensuring persistence across sessions.

### Key Features
- **Workout Logging:** Record exercise, sets, reps, and weight through an interactive menu.  
- **Progress Visualization:** View dual-axis charts of reps and weights over time (Matplotlib).  
- **Persistent Storage:** Data saved automatically in CSV and JSON.  
- **Simple CLI:** Lightweight, easy-to-navigate interface.  
- **Extensible Design:** Modular structure with GUI support via `gui_tracker.py`.

---

## Built With

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib](https://matplotlib.org/)
- [CSV / JSON](https://docs.python.org/3/library/csv.html)

---

## Getting Started

Follow these steps to set up a local copy of the project.

### Prerequisites
- Python 3.8+  
- Tkinter (included by default)  

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dereksun00/gym-tracker.git
   cd gym-tracker

2. **Run the app**
   ```bash
   python main.py

---

## Usage

1. Launch the app:
   Once you launch the program, you'll see a console menu.
   ```bash
   ---- Gym Tracker ----
   1. View Program
   2. Add Exercise(s)
   3. Log Workout
   4. View Log
   5. Remove Log Entry
   6. Remove Exercise
   7. View Progress Chart
   8. Exit

- Follow on-screen prompts to add or log workouts.
- Logs are saved in workouts.csv and program.json.
- Select “View Progress Chart” to visualize your data.

---

## Roadmap

- Add graphs for visual progress tracking
- Implement user profiles
- Switch to SQLite for more robust storage
- Add export-to-Excel option
- Introduce a dark mode for the UI

---

## Contact

Derek Sun - sunderek3602@gmail.com
Project Link: https://github.com/dereksun00
