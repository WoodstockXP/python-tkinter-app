import tkinter as tk
from tkinter import ttk, messagebox

from database import DatabaseConnection
from exceptions import ValidationException, DatabaseException, LogicException
from player import Player
from team import Team
from tournament import Tournament

class TournamentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flash Tournament Management System | Pro Edition")
        self.geometry("1000x650") # Made the window larger for the split view
        
        # Apply a modern theme and styling
        self._apply_styling()

        try:
            self.db = DatabaseConnection()
            self._patch_database() # Ensure enrollment table exists
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Could not connect to database: {e}")
            self.destroy()

        self._build_gui()
        self._refresh_all_data() # Load data immediately on startup

    def _apply_styling(self):
        """Adds visual impact to the dull default Tkinter UI."""
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
            
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#2c3e50")
        
        # Style buttons
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#0d6efd", foreground="white", padding=6)
        style.map("Action.TButton", background=[("active", "#0b5ed7")])

        # Style Treeview (Data Tables)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e9ecef")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    def _patch_database(self):
        """Silently adds a bridging table to track enrollments if it doesn't exist."""
        query = '''CREATE TABLE IF NOT EXISTS tournament_enrollments (
                    tournament_id INTEGER, participant_id INTEGER,
                    PRIMARY KEY (tournament_id, participant_id),
                    FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
                    FOREIGN KEY (participant_id) REFERENCES participants(id)
                   )'''
        self.db.execute_query(query)

    def _build_gui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # ==========================================
        # TAB 1: PARTICIPANTS (Split Layout)
        # ==========================================
        part_tab = ttk.Frame(notebook)
        notebook.add(part_tab, text="👤 Manage Participants")
        
        # LEFT: Form
        p_left = ttk.Frame(part_tab, padding=20)
        p_left.pack(side="left", fill="y")
        
        ttk.Label(p_left, text="Register New Entity", style="Header.TLabel").pack(anchor="w", pady=(0, 15))
        
        ttk.Label(p_left, text="Name:").pack(anchor="w")
        self.name_entry = ttk.Entry(p_left, width=35)
        self.name_entry.pack(pady=(0, 10))

        ttk.Label(p_left, text="Type:").pack(anchor="w")
        type_frame = ttk.Frame(p_left)
        type_frame.pack(anchor="w", pady=(0, 10))
        self.type_var = tk.StringVar(value="Player")
        ttk.Radiobutton(type_frame, text="Player", variable=self.type_var, value="Player").pack(side="left", padx=(0, 15))
        ttk.Radiobutton(type_frame, text="Team", variable=self.type_var, value="Team").pack(side="left")

        ttk.Label(p_left, text="Nickname (Players Only):").pack(anchor="w")
        self.nick_entry = ttk.Entry(p_left, width=35)
        self.nick_entry.pack(pady=(0, 20))

        ttk.Button(p_left, text="➕ Save Participant", style="Action.TButton", command=self.register_participant).pack(fill="x")

        # RIGHT: Dashboard (Treeview)
        p_right = ttk.Frame(part_tab, padding=20)
        p_right.pack(side="right", expand=True, fill="both")
        
        ttk.Label(p_right, text="Participant Database", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.p_tree = ttk.Treeview(p_right, columns=("ID", "Name", "Type", "Details"), show="headings")
        self.p_tree.heading("ID", text="ID")
        self.p_tree.heading("Name", text="Name")
        self.p_tree.heading("Type", text="Type")
        self.p_tree.heading("Details", text="Nickname/Rank")
        
        self.p_tree.column("ID", width=50, anchor="center")
        self.p_tree.column("Type", width=80, anchor="center")
        self.p_tree.pack(expand=True, fill="both")

        # ==========================================
        # TAB 2: TOURNAMENTS (Split Layout)
        # ==========================================
        tourn_tab = ttk.Frame(notebook)
        notebook.add(tourn_tab, text="🏆 Manage Tournaments")

        # LEFT: Forms
        t_left = ttk.Frame(tourn_tab, padding=20)
        t_left.pack(side="left", fill="y")

        # Section 2A: Create
        ttk.Label(t_left, text="1. Create Tournament", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(t_left, text="Tournament Name:").pack(anchor="w")
        self.t_name_entry = ttk.Entry(t_left, width=35)
        self.t_name_entry.pack(pady=(0, 10))
        ttk.Button(t_left, text="➕ Create", style="Action.TButton", command=self.create_tournament).pack(fill="x", pady=(0, 25))

        # Section 2B: Enroll
        ttk.Label(t_left, text="2. Enroll Participants", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(t_left, text="Select Tournament:").pack(anchor="w")
        self.t_combo = ttk.Combobox(t_left, state="readonly", width=33)
        self.t_combo.pack(pady=(0, 10))
        
        ttk.Label(t_left, text="Select Participant:").pack(anchor="w")
        self.p_combo = ttk.Combobox(t_left, state="readonly", width=33)
        self.p_combo.pack(pady=(0, 15))
        
        ttk.Button(t_left, text="🔗 Enroll Selected", style="Action.TButton", command=self.enroll_participant).pack(fill="x")

        # RIGHT: Dashboard
        t_right = ttk.Frame(tourn_tab, padding=20)
        t_right.pack(side="right", expand=True, fill="both")

        ttk.Label(t_right, text="Tournament Database", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.t_tree = ttk.Treeview(t_right, columns=("ID", "Name", "Status"), show="headings")
        self.t_tree.heading("ID", text="ID")
        self.t_tree.heading("Name", text="Tournament Name")
        self.t_tree.heading("Status", text="Status")
        self.t_tree.column("ID", width=50, anchor="center")
        self.t_tree.pack(expand=True, fill="both")

    # --- DATA REFRESH LOGIC ---

    def _refresh_all_data(self):
        """Fetches data from DB and updates all tables and dropdowns."""
        # 1. Update Participants Treeview & Combobox
        for row in self.p_tree.get_children():
            self.p_tree.delete(row)
            
        participants = self.db.fetch_all("SELECT id, name, type, nickname, ranking FROM participants")
        combo_participants = []
        for p in participants:
            details = p[3] if p[2] == "Player" else f"Rank: {p[4]}"
            self.p_tree.insert("", tk.END, values=(p[0], p[1], p[2], details))
            combo_participants.append(f"{p[0]} - {p[1]} ({p[2]})")
            
        self.p_combo['values'] = combo_participants

        # 2. Update Tournaments Treeview & Combobox
        for row in self.t_tree.get_children():
            self.t_tree.delete(row)
            
        tournaments = self.db.fetch_all("SELECT id, name, status FROM tournaments")
        combo_tournaments = []
        for t in tournaments:
            self.t_tree.insert("", tk.END, values=(t[0], t[1], t[2]))
            combo_tournaments.append(f"{t[0]} - {t[1]}")
            
        self.t_combo['values'] = combo_tournaments

    # --- CONTROLLER LOGIC ---

    def register_participant(self):
        try:
            name = self.name_entry.get().strip()
            p_type = self.type_var.get()
            nickname = self.nick_entry.get().strip()

            if not name:
                raise ValidationException("Participant name cannot be empty!")

            query = "INSERT INTO participants (name, type, nickname, ranking) VALUES (?, ?, ?, ?)"
            self.db.execute_query(query, (name, p_type, nickname if p_type == "Player" else None, 1000))
            
            self.name_entry.delete(0, tk.END)
            self.nick_entry.delete(0, tk.END)
            self._refresh_all_data() # Instantly show the new user in the UI!
            messagebox.showinfo("Success", f"{p_type} '{name}' registered.")

        except ValidationException as ve:
            messagebox.showwarning("Validation Error", ve.message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_tournament(self):
        try:
            name = self.t_name_entry.get().strip()
            if not name:
                raise ValidationException("Tournament name cannot be empty!")

            self.db.execute_query("INSERT INTO tournaments (name) VALUES (?)", (name,))
            self.t_name_entry.delete(0, tk.END)
            self._refresh_all_data() # Instantly show the new tournament!
            messagebox.showinfo("Success", f"Tournament '{name}' created!")

        except Exception as e:
            messagebox.showwarning("Error", str(e))

    def enroll_participant(self):
        try:
            t_selection = self.t_combo.get()
            p_selection = self.p_combo.get()
            
            if not t_selection or not p_selection:
                raise ValidationException("Please select BOTH a tournament and a participant.")

            # Extract IDs from the combobox strings (e.g., "1 - Global Cup" -> 1)
            t_id = int(t_selection.split(" - ")[0])
            p_id = int(p_selection.split(" - ")[0])

            self.db.execute_query("INSERT INTO tournament_enrollments (tournament_id, participant_id) VALUES (?, ?)", (t_id, p_id))
            messagebox.showinfo("Success", "Participant successfully enrolled in the tournament!")

        except DatabaseException:
            messagebox.showwarning("Duplicate", "This participant is already enrolled in this tournament.")
        except ValidationException as ve:
            messagebox.showwarning("Validation Error", ve.message)

if __name__ == "__main__":
    app = TournamentApp()
    app.mainloop()