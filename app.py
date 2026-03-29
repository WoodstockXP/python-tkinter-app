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
        self.geometry("1050x750") 
        
        self._apply_styling()

        try:
            self.db = DatabaseConnection()
            self._patch_database() 
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Could not connect to database: {e}")
            self.destroy()

        self._build_gui()
        self._refresh_all_data()

    def _apply_styling(self):
        """Applies a modern, high-contrast, flat-design theme to the GUI."""
        # Set the absolute background of the main window to a soft slate gray
        self.configure(bg="#f1f5f9") 
        
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
            
        # Base Container Styling (Make inner frames look like clean white cards)
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 11), foreground="#334155")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#0f172a")
        
        # Notebook (Tabs) Styling
        style.configure("TNotebook", background="#f1f5f9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[25, 12], background="#e2e8f0", foreground="#64748b", borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[("selected", "#ffffff")], 
                  foreground=[("selected", "#2563eb")]) # Active tab turns blue and white
        
        # Primary Action Buttons (Vibrant Blue)
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), background="#2563eb", foreground="white", borderwidth=0, padding=8)
        style.map("Action.TButton", 
                  background=[("active", "#1d4ed8")], 
                  foreground=[("active", "white")])

        # Danger Button (Crisp Red)
        style.configure("Danger.TButton", font=("Segoe UI", 11, "bold"), background="#ef4444", foreground="white", borderwidth=0, padding=8)
        style.map("Danger.TButton", 
                  background=[("active", "#dc2626")], 
                  foreground=[("active", "white")])

        # Radio Buttons
        style.configure("TRadiobutton", background="#ffffff", font=("Segoe UI", 11), foreground="#334155")
        style.map("TRadiobutton", background=[("active", "#ffffff")])

        # Data Tables (Treeview)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=32, background="#ffffff", fieldbackground="#ffffff", borderwidth=0)
        style.map("Treeview", 
                  background=[('selected', '#dbeafe')], # Soft blue highlight on click
                  foreground=[('selected', '#1e40af')]) # Deep blue text on click
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#f8fafc", foreground="#0f172a", padding=6)

    def _patch_database(self):
        query = '''CREATE TABLE IF NOT EXISTS tournament_enrollments (
                    tournament_id INTEGER, participant_id INTEGER,
                    PRIMARY KEY (tournament_id, participant_id),
                    FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
                    FOREIGN KEY (participant_id) REFERENCES participants(id)
                   )'''
        self.db.execute_query(query)

    def _build_gui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=10, pady=(10, 0))

        # ==========================================
        # TAB 1: PARTICIPANTS
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

        # RIGHT: Master-Detail Dashboard
        p_right = ttk.Frame(part_tab, padding=20)
        p_right.pack(side="right", expand=True, fill="both")
        
        # Top Table: All Participants
        ttk.Label(p_right, text="Participant Database (Click a row to see details)", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.p_tree = ttk.Treeview(p_right, columns=("ID", "Name", "Type", "Details"), show="headings", height=8)
        self.p_tree.heading("ID", text="ID"); self.p_tree.column("ID", width=50, anchor="center")
        self.p_tree.heading("Name", text="Name")
        self.p_tree.heading("Type", text="Type"); self.p_tree.column("Type", width=80, anchor="center")
        self.p_tree.heading("Details", text="Nickname/Rank")
        self.p_tree.pack(fill="x", pady=(0, 20))
        self.p_tree.bind("<<TreeviewSelect>>", self._on_participant_select) # Bind click event

        # Bottom Table: Participant's Tournaments
        ttk.Label(p_right, text="Currently Enrolled In:", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.p_sub_tree = ttk.Treeview(p_right, columns=("ID", "Tournament Name", "Status"), show="headings", height=5)
        self.p_sub_tree.heading("ID", text="T-ID"); self.p_sub_tree.column("ID", width=50, anchor="center")
        self.p_sub_tree.heading("Tournament Name", text="Tournament Name")
        self.p_sub_tree.heading("Status", text="Status"); self.p_sub_tree.column("Status", width=100, anchor="center")
        self.p_sub_tree.pack(fill="x")

        # ==========================================
        # TAB 2: TOURNAMENTS
        # ==========================================
        tourn_tab = ttk.Frame(notebook)
        notebook.add(tourn_tab, text="🏆 Manage Tournaments")

        # LEFT: Forms
        t_left = ttk.Frame(tourn_tab, padding=20)
        t_left.pack(side="left", fill="y")

        ttk.Label(t_left, text="1. Create Tournament", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(t_left, text="Tournament Name:").pack(anchor="w")
        self.t_name_entry = ttk.Entry(t_left, width=35)
        self.t_name_entry.pack(pady=(0, 10))
        ttk.Button(t_left, text="➕ Create", style="Action.TButton", command=self.create_tournament).pack(fill="x", pady=(0, 25))

        ttk.Label(t_left, text="2. Enroll Participants", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(t_left, text="Select Tournament:").pack(anchor="w")
        self.t_combo = ttk.Combobox(t_left, state="readonly", width=33)
        self.t_combo.pack(pady=(0, 10))
        
        ttk.Label(t_left, text="Select Participant:").pack(anchor="w")
        self.p_combo = ttk.Combobox(t_left, state="readonly", width=33)
        self.p_combo.pack(pady=(0, 15))
        ttk.Button(t_left, text="🔗 Enroll Selected", style="Action.TButton", command=self.enroll_participant).pack(fill="x")

        # RIGHT: Master-Detail Dashboard
        t_right = ttk.Frame(tourn_tab, padding=20)
        t_right.pack(side="right", expand=True, fill="both")

        # Top Table: All Tournaments
        ttk.Label(t_right, text="Tournament Database (Click a row to see roster)", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.t_tree = ttk.Treeview(t_right, columns=("ID", "Name", "Status"), show="headings", height=8)
        self.t_tree.heading("ID", text="ID"); self.t_tree.column("ID", width=50, anchor="center")
        self.t_tree.heading("Name", text="Tournament Name")
        self.t_tree.heading("Status", text="Status"); self.t_tree.column("Status", width=100, anchor="center")
        self.t_tree.pack(fill="x", pady=(0, 20))
        self.t_tree.bind("<<TreeviewSelect>>", self._on_tournament_select) # Bind click event

        # Bottom Table: Tournament's Roster
        ttk.Label(t_right, text="Enrolled Roster:", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.t_sub_tree = ttk.Treeview(t_right, columns=("ID", "Name", "Type"), show="headings", height=5)
        self.t_sub_tree.heading("ID", text="P-ID"); self.t_sub_tree.column("ID", width=50, anchor="center")
        self.t_sub_tree.heading("Name", text="Participant Name")
        self.t_sub_tree.heading("Type", text="Type"); self.t_sub_tree.column("Type", width=100, anchor="center")
        self.t_sub_tree.pack(fill="x")

        # ==========================================
        # FOOTER: DANGER ZONE
        # ==========================================
        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=10, pady=10)
        ttk.Button(footer, text="🗑️ CLEAR ENTIRE DATABASE", style="Danger.TButton", command=self.clear_database).pack(side="right")

    # --- EVENT HANDLERS (CLICKING ON TABLES) ---

    def _on_participant_select(self, event):
        """Fires when a user clicks a row in the Participant table."""
        selected = self.p_tree.selection()
        if not selected: return
        p_id = self.p_tree.item(selected[0])['values'][0]
        
        # Clear the sub-table
        for row in self.p_sub_tree.get_children(): self.p_sub_tree.delete(row)
        
        # Fetch their tournaments via SQL JOIN
        query = """SELECT t.id, t.name, t.status FROM tournaments t 
                   JOIN tournament_enrollments te ON t.id = te.tournament_id 
                   WHERE te.participant_id = ?"""
        for t in self.db.fetch_all(query, (p_id,)):
            self.p_sub_tree.insert("", tk.END, values=(t[0], t[1], t[2]))

    def _on_tournament_select(self, event):
        """Fires when a user clicks a row in the Tournament table."""
        selected = self.t_tree.selection()
        if not selected: return
        t_id = self.t_tree.item(selected[0])['values'][0]
        
        # Clear the sub-table
        for row in self.t_sub_tree.get_children(): self.t_sub_tree.delete(row)
        
        # Fetch enrolled participants via SQL JOIN
        query = """SELECT p.id, p.name, p.type FROM participants p 
                   JOIN tournament_enrollments te ON p.id = te.participant_id 
                   WHERE te.tournament_id = ?"""
        for p in self.db.fetch_all(query, (t_id,)):
            self.t_sub_tree.insert("", tk.END, values=(p[0], p[1], p[2]))

    # --- DATA REFRESH LOGIC ---

    def _refresh_all_data(self):
        for row in self.p_tree.get_children(): self.p_tree.delete(row)
        combo_participants = []
        for p in self.db.fetch_all("SELECT id, name, type, nickname, ranking FROM participants"):
            details = p[3] if p[2] == "Player" else f"Rank: {p[4]}"
            self.p_tree.insert("", tk.END, values=(p[0], p[1], p[2], details))
            combo_participants.append(f"{p[0]} - {p[1]} ({p[2]})")
        self.p_combo['values'] = combo_participants

        for row in self.t_tree.get_children(): self.t_tree.delete(row)
        combo_tournaments = []
        for t in self.db.fetch_all("SELECT id, name, status FROM tournaments"):
            self.t_tree.insert("", tk.END, values=(t[0], t[1], t[2]))
            combo_tournaments.append(f"{t[0]} - {t[1]}")
        self.t_combo['values'] = combo_tournaments

        # Clear sub-tables on master refresh
        for row in self.p_sub_tree.get_children(): self.p_sub_tree.delete(row)
        for row in self.t_sub_tree.get_children(): self.t_sub_tree.delete(row)

    # --- CONTROLLER LOGIC ---

    def register_participant(self):
        try:
            name = self.name_entry.get().strip()
            p_type = self.type_var.get()
            nickname = self.nick_entry.get().strip()
            if not name: raise ValidationException("Participant name cannot be empty!")
            self.db.execute_query("INSERT INTO participants (name, type, nickname, ranking) VALUES (?, ?, ?, ?)", (name, p_type, nickname if p_type == "Player" else None, 1000))
            self.name_entry.delete(0, tk.END)
            self.nick_entry.delete(0, tk.END)
            self._refresh_all_data()
            messagebox.showinfo("Success", f"{p_type} '{name}' registered.")
        except ValidationException as ve: messagebox.showwarning("Validation Error", ve.message)
        except Exception as e: messagebox.showerror("Error", str(e))

    def create_tournament(self):
        try:
            name = self.t_name_entry.get().strip()
            if not name: raise ValidationException("Tournament name cannot be empty!")
            self.db.execute_query("INSERT INTO tournaments (name) VALUES (?)", (name,))
            self.t_name_entry.delete(0, tk.END)
            self._refresh_all_data()
            messagebox.showinfo("Success", f"Tournament '{name}' created!")
        except Exception as e: messagebox.showwarning("Error", str(e))

    def enroll_participant(self):
        try:
            if not self.t_combo.get() or not self.p_combo.get():
                raise ValidationException("Select BOTH a tournament and a participant.")
            t_id = int(self.t_combo.get().split(" - ")[0])
            p_id = int(self.p_combo.get().split(" - ")[0])
            self.db.execute_query("INSERT INTO tournament_enrollments (tournament_id, participant_id) VALUES (?, ?)", (t_id, p_id))
            
            # Simulate a click on the tournament to refresh the sub-table instantly
            self._on_tournament_select(None)
            messagebox.showinfo("Success", "Enrolled successfully!")
        except DatabaseException: messagebox.showwarning("Duplicate", "Already enrolled in this tournament.")
        except ValidationException as ve: messagebox.showwarning("Validation Error", ve.message)

    def clear_database(self):
        """Safely wipes all tables if the user confirms."""
        confirm = messagebox.askyesno("⚠️ DANGER ZONE", "Are you absolutely sure you want to DELETE ALL DATA?\n\nThis will wipe all users, teams, matches, and tournaments. This cannot be undone!")
        if confirm:
            try:
                # Delete in correct order to avoid foreign key conflicts
                self.db.execute_query("DELETE FROM tournament_enrollments")
                self.db.execute_query("DELETE FROM matches")
                self.db.execute_query("DELETE FROM tournaments")
                self.db.execute_query("DELETE FROM participants")
                self._refresh_all_data()
                messagebox.showinfo("Wiped", "Database has been completely cleared.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to clear database: {e}")

if __name__ == "__main__":
    app = TournamentApp()
    app.mainloop()