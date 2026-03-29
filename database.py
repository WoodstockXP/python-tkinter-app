import sqlite3
from sqlite3 import Error

class DatabaseConnection:
    # Private class attribute to hold the single instance
    __instance = None

    def __new__(cls):
        """
        Overrides the built-in __new__ method to implement the Singleton pattern.
        If an instance already exists, it returns it. Otherwise, it creates one.
        """
        if cls.__instance is None:
            cls.__instance = super(DatabaseConnection, cls).__new__(cls)
            cls.__instance._init_db()
        return cls.__instance

    def _init_db(self):
        """Initializes the SQLite connection and creates the required tables."""
        self.db_name = "tournament_data.db"
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self._create_tables()
        except Error as e:
            print(f"Database connection error: {e}")

    def _create_tables(self):
        """Creates the Participants, Tournaments, and Matches tables if they don't exist."""
        
        # 1. Participants Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL, -- 'Player' or 'Team'
                nickname TEXT,
                ranking INTEGER
            )
        ''')

        # 2. Tournaments Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'Scheduled'
            )
        ''')

        # 3. Matches Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                tournament_id INTEGER,
                participant1_id INTEGER,
                participant2_id INTEGER,
                score TEXT,
                winner_id INTEGER,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
                FOREIGN KEY (participant1_id) REFERENCES participants (id),
                FOREIGN KEY (participant2_id) REFERENCES participants (id),
                FOREIGN KEY (winner_id) REFERENCES participants (id)
            )
        ''')
        self.connection.commit()

    def get_connection(self):
        """Returns the active database connection."""
        return self.connection

    def execute_query(self, query: str, parameters: tuple = ()):
        """Helper method to safely execute INSERT/UPDATE/DELETE queries."""
        try:
            self.cursor.execute(query, parameters)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Query execution error: {e}")
            raise e

    def fetch_all(self, query: str, parameters: tuple = ()):
        """Helper method to safely execute SELECT queries."""
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Data fetch error: {e}")
            raise e