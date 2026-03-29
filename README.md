# Flash Tournament Management System

A robust, Python-based desktop application designed to manage academic and social tournaments. This system allows organizers to register players and teams, create tournaments, and track enrollments using a modern graphical interface backed by a relational database.

This project was developed as a comprehensive case study to demonstrate the practical application of Object-Oriented Programming (OOP) principles and Layered Software Architecture.

---

## Features

### User-Facing Features (Pro Edition)
* **Modern GUI:** A clean, tabbed interface utilizing the `ttk` 'clam' theme.
* **Master-Detail Dashboards:** Click on any participant or tournament to instantly view their specific enrollments and rosters dynamically.
* **Dual Registration:** Register individual Players (with nicknames) or entire Teams.
* **Tournament Enrollment:** Link existing participants to scheduled tournaments.
* **Safe Reset:** A "Danger Zone" feature to safely wipe the database with confirmation dialogs.

### Technical & Architectural Features
* **Layered Architecture:** Clear separation between Presentation (GUI), Business Logic (OOP Models), and Persistence (SQLite) layers.
* **Singleton Database Pattern:** Ensures only one active connection to the SQLite database exists, optimizing memory and preventing file locks.
* **Custom Exception Hierarchy:** Domain-specific error handling (`ValidationException`, `DatabaseException`, `LogicException`) prevents crashes and feeds user-friendly alerts to the GUI.
* **Automated Migrations:** The system automatically builds the necessary relational tables (`participants`, `tournaments`, `matches`, `tournament_enrollments`) upon the first launch.

---

## Object-Oriented Principles Applied

This system strictly adheres to the four pillars of OOP:

1. **Abstraction:** Implemented via the `Participant` Abstract Base Class (ABC). It defines the blueprint and enforces the implementation of the `register()` method without allowing direct instantiation.
2. **Encapsulation:** All class attributes (e.g., `__id`, `__name`, `__player_list`) are strictly private, accessible only through defined getter/setter methods to protect data integrity.
3. **Inheritance:** Both `Player` and `Team` concrete classes inherit core attributes and methods from the `Participant` base class, extending them with their own specific needs.
4. **Polymorphism:** The `Match` and `Tournament` classes interact with the base `Participant` type. This allows the system to seamlessly pit a Player vs Player or a Team vs Team using the exact same logic.

---

## Project Structure

flash_tournament/
|
|-- app.py              # Presentation Layer (Tkinter GUI & Controller)
|-- database.py         # Persistence Layer (SQLite Singleton)
|-- exceptions.py       # Custom Error Management Hierarchy
|
|-- participant.py      # Abstract Base Class
|-- player.py           # Concrete Class (Inherits Participant)
|-- team.py             # Concrete Class (Inherits Participant)
|
|-- match.py            # Core Logic Class
|-- tournament.py       # Core Logic Class
|
|-- README.md           # Project Documentation

---

## Installation & Setup

Because this project relies entirely on Python's robust standard library, there are **no external dependencies or pip packages to install.**

1. Ensure you have **Python 3.8+** installed on your machine.
2. Clone or download this repository.
3. Open your terminal or command prompt, navigate to the project folder, and run:

python app.py

*(Note: A local SQLite database file named `tournament_data.db` will be automatically generated in the same folder upon your first launch).*

---

## User Guide

### 1. Registering Participants
1. Navigate to the **"Manage Participants"** tab.
2. Enter a Name.
3. Select the Type (`Player` or `Team`). If registering a Player, you may optionally provide a Nickname.
4. Click **"Save Participant"**. They will immediately appear in the database table on the right.

### 2. Creating a Tournament
1. Navigate to the **"Manage Tournaments"** tab.
2. Under the "1. Create Tournament" section, enter a name for your event (e.g., "Spring Smash 2026").
3. Click **"Create"**. It will appear in the Tournament Database table on the right.

### 3. Enrolling Participants
1. Stay on the **"Manage Tournaments"** tab.
2. Under the "2. Enroll Participants" section, use the dropdown menus to select an existing Tournament and an existing Participant.
3. Click **"Enroll Selected"**.

### 4. Viewing Data (Master-Detail View)
* **To see a Tournament's Roster:** Click on any tournament in the upper-right table. The sub-table below it will instantly populate with all enrolled players/teams.
* **To see a Participant's History:** Go to the Participants tab and click on any user. The sub-table will show every tournament they are currently enrolled in.

### 5. Resetting the System
If you need to start fresh for a new semester or wipe test data, scroll to the bottom of the application window and click the red **"CLEAR ENTIRE DATABASE"** button. *Note: This action is permanent and cannot be undone.*