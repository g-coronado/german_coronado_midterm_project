# **README.md**

# **german_coronado_midterm_project**  
**CPRO 2201 – Python Programming II**  
**Baseball Team Manager – Midterm Project**

## **Baseball Team Manager**

A desktop application built with **Python** and **Tkinter** for managing a baseball team lineup, player statistics, and defensive positions. The project follows a simple MVC-style structure and uses an SQLite database for persistent storage.

GitHub Repository:  
**https://github.com/g-coronado/german_coronado_midterm_project**

---

## **Features**

### **Player Management**
- Add new players with first name, last name, position, at-bats, and hits.
- Remove players by ID.
- Edit player statistics (At Bats and Hits) with validation.
- Edit defensive positions using a list of valid positions from the database.

### **Lineup Display**
- View all players in a sortable table (TreeView).
- Displays batting order, names, position, at-bats, hits, and batting average.

### **Game Date Tracking**
- Prompts for a game date on startup.
- Calculates and displays the number of days remaining until the game.

### **User Interface**
- Built with Tkinter using frames, labels, buttons, and modal popup windows.
- Popups stay on top of the main window and block interaction until closed.
- Clean layout with left‑aligned labels and consistent spacing.

---

## **Project Structure**

```
project/
│
├── ui.py          # Main Tkinter UI and controller logic (RUN THIS FILE)
├── db.py          # Database connection and SQL operations
├── objects.py     # Player class definition
├── players.db     # SQLite database (auto-created if missing)
└── README.md      # Project documentation
```

---

## **Repository Branches**

This project contains **four branches**, each representing a required section of the midterm assignment:

- **section1** — Initial setup, database creation, and basic structure  
- **section2** — Core functionality and controller logic  
- **section3** — User interface development and event handling  
- **section4** — Final integration, validation rules, and polishing  

The **main branch** contains the fully integrated and completed version of the project.

---

## **Database Schema**

The application uses an SQLite database named **`players.db`** with two tables: **Player** and **Position**.

### **Player Table**

Stores all player information, including batting order and statistics.

```sql
CREATE TABLE Player(
    playerID   INTEGER PRIMARY KEY NOT NULL,
    batOrder   INTEGER NOT NULL,
    firstName  TEXT NOT NULL,
    lastName   TEXT NOT NULL,
    position   TEXT NOT NULL,
    atBats     INTEGER NULL,
    hits       INTEGER NULL
);
```

### **Position Table**

Stores the list of valid defensive positions.

```sql
CREATE TABLE Position(
    positionID   INTEGER NOT NULL PRIMARY KEY,
    positionName TEXT NOT NULL
);
```

### **Schema Notes**
- `playerID` uniquely identifies each player.
- `batOrder` determines the batting lineup order.
- `positionName` in the `Position` table must match the `position` field in the `Player` table.
- `atBats` and `hits` may be `NULL`, but the UI enforces validation to prevent negative values or invalid combinations.

---

## **Requirements**

- Python 3.8+
- Tkinter (included with most Python installations)
- SQLite3 (included with Python)

No external libraries are required.

---

## **How to Run**

The application **must be started from `ui.py`**.

1. Clone the repository:

```bash
git clone https://github.com/g-coronado/german_coronado_midterm_project.git
```

2. Navigate into the project folder:

```bash
cd german_coronado_midterm_project
```

3. Run the program:

```bash
python ui.py
```

4. Enter the game date when prompted.

5. The main window will open after the date is confirmed.

---

## **Validation Rules**

The application enforces several input rules:

- First and last names must contain only alphabetic characters.
- Position must be one of the valid positions stored in the database.
- At Bats and Hits must be numeric.
- At Bats and Hits cannot be negative.
- Hits cannot exceed At Bats.
- Player ID must be numeric when editing or removing players.

---

## **Notes**

- Batting order is automatically assigned based on the number of players.
- Changing the batting order manually is intentionally disabled.
- All popup windows are modal and stay in front of the main window.
- The UI is designed to be simple, clean, and easy to use.

---

## **License**

This project is provided for educational purposes.  
You may modify or extend it as needed.


