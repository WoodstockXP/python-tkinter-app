class TournamentAppException(Exception):
    """
    Base exception class for the Tournament Application.
    All custom exceptions will inherit from this base class.
    """
    pass

class ValidationException(TournamentAppException):
    """
    Handles incorrect user inputs in the GUI.
    Example: Leaving a required field blank or entering text in a number field.
    """
    def __init__(self, message="Invalid input provided in the interface."):
        self.message = message
        super().__init__(self.message)

class DatabaseException(TournamentAppException):
    """
    Manages connectivity issues and query errors in the Persistence Layer.
    Example: Failing to connect to SQLite or a constraint violation.
    """
    def __init__(self, message="A database error occurred."):
        self.message = message
        super().__init__(self.message)

class LogicException(TournamentAppException):
    """
    Prevents illegal states in the Business Logic Layer.
    Example: Attempting to generate tournament brackets with less than 2 players.
    """
    def __init__(self, message="An illegal logic operation was attempted."):
        self.message = message
        super().__init__(self.message)