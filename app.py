import tkinter as tk
from tkinter import ttk, messagebox

# Import our custom modules
from database import DatabaseConnection
from exceptions import ValidationException, DatabaseException, LogicException
from player import Player
from team import Team
from tournament import Tournament

class TournamentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flash Tournament Management System")
        self.geometry("600x450")
        
        # 1. Initialize Database (Singleton)
        try:
            self.db = DatabaseConnection()
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Could not connect to database: {e}")
            self.destroy()

        self._build_gui()

    def _build_gui(self):
        """Constructs the Tkinter Notebook (Tabs) and widgets."""
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- TAB 1: Participants ---
        part_frame = ttk.Frame(notebook)
        notebook.add(part_frame, text="Register Participant")

        ttk.Label(part_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(part_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(part_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_var = tk.StringVar(value="Player")
        ttk.Radiobutton(part_frame, text="Player", variable=self.type_var, value="Player").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(part_frame, text="Team", variable=self.type_var, value="Team").grid(row=1, column=1, padx=80, sticky="w")

        ttk.Label(part_frame, text="Nickname (Player Only):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.nick_entry = ttk.Entry(part_frame, width=30)
        self.nick_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(part_frame, text="Register Participant", command=self.register_participant).grid(row=3, column=0, columnspan=2, pady=20)

        # --- TAB 2: Tournaments ---
        tourn_frame = ttk.Frame(notebook)
        notebook.add(tourn_frame, text="Tournaments")

        ttk.Label(tourn_frame, text="Tournament Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.t_name_entry = ttk.Entry(tourn_frame, width=30)
        self.t_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(tourn_frame, text="Create Tournament", command=self.create_tournament).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(tourn_frame, text="Test Logic Exception (Generate Brackets)", command=self.test_logic_exception).grid(row=2, column=0, columnspan=2, pady=10)

    # --- CONTROLLER LOGIC ---

    def register_participant(self):
        """Reads GUI inputs, validates, creates objects, and saves to DB."""
        try:
            name = self.name_entry.get().strip()
            p_type = self.type_var.get()
            nickname = self.nick_entry.get().strip()

            # Trigger ValidationException if name is blank
            if not name:
                raise ValidationException("Participant name cannot be empty!")

            # Database Insertion
            query = "INSERT INTO participants (name, type, nickname, ranking) VALUES (?, ?, ?, ?)"
            params = (name, p_type, nickname if p_type == "Player" else None, 1000)
            
            # This might raise a DatabaseException (handled below)
            new_id = self.db.execute_query(query, params)

            # Object Creation (Demonstrating OOP usage)
            if p_type == "Player":
                new_participant = Player(new_id, name, nickname, 1000)
            else:
                new_participant = Team(new_id, name)

            # Success message using the object's polymorphic register() method
            messagebox.showinfo("Success", new_participant.register())
            
            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.nick_entry.delete(0, tk.END)

        except ValidationException as ve:
            messagebox.showwarning("Validation Error", ve.message)
        except DatabaseException as de:
            messagebox.showerror("Database Error", de.message)
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))

    def create_tournament(self):
        """Creates a new tournament in the database."""
        try:
            name = self.t_name_entry.get().strip()
            if not name:
                raise ValidationException("Tournament name cannot be empty!")

            query = "INSERT INTO tournaments (name) VALUES (?)"
            self.db.execute_query(query, (name,))
            messagebox.showinfo("Success", f"Tournament '{name}' created successfully!")
            self.t_name_entry.delete(0, tk.END)

        except ValidationException as ve:
            messagebox.showwarning("Validation Error", ve.message)
        except DatabaseException as de:
            messagebox.showerror("Database Error", de.message)

    def test_logic_exception(self):
        """Demonstrates the Business Logic exception handling."""
        try:
            # We create an empty tournament to force the LogicException
            temp_tourn = Tournament(99, "Temp Tournament")
            
            # This will fail because there are 0 participants
            temp_tourn.generateBrackets() 

        except LogicException as le:
            messagebox.showwarning("Logic Error", le.message)

if __name__ == "__main__":
    app = TournamentApp()
    app.mainloop()