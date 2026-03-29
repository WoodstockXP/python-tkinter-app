from participant import Participant
from match import Match
from exceptions import LogicException

class Tournament:
    def __init__(self, tournament_id: int, name: str):
        self.__id = tournament_id
        self.__name = name
        self.__participants = []  # List to hold Participant objects
        self.__matches = []       # List to hold Match objects

    def registerParticipant(self, participant: Participant):
        """Adds a participant (Player or Team) to the tournament."""
        self.__participants.append(participant)
        return f"Successfully registered '{participant.get_name()}' to tournament '{self.__name}'."

    def generateBrackets(self):
        """
        Generates first-round matches automatically. 
        Note: We will add custom Exception handling here in Step 5.
        """
        if len(self.__participants) < 2:
            raise LogicException("Not enough participants to generate brackets.")
            
        self.__matches.clear()
        match_id = 1
        
        # Simple pairing logic: pairs participant 1 with 2, 3 with 4, etc.
        for i in range(0, len(self.__participants) - 1, 2):
            p1 = self.__participants[i]
            p2 = self.__participants[i+1]
            new_match = Match(match_id, p1, p2)
            self.__matches.append(new_match)
            match_id += 1
            
        return f"Generated {len(self.__matches)} matches for the first round."

    def getWinner(self):
        """Returns the overall winner of the tournament."""
        if not self.__matches:
            return "No matches have been played yet."
            
        # For simplicity in this step, we check the last match in the list
        last_match_winner = self.__matches[-1].getWinner()
        if last_match_winner:
            return f"Tournament Champion: {last_match_winner.get_name()}!"
        return "Tournament is still in progress."
        
    def show_matches(self):
        """Helper method to print all matches."""
        return [match.get_details() for match in self.__matches]