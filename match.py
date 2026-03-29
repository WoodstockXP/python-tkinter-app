from participant import Participant

class Match:
    def __init__(self, match_id: int, participant1: Participant, participant2: Participant):
        self.__id = match_id
        self.__participant1 = participant1
        self.__participant2 = participant2
        self.__score = ""
        self.__winner = None

    def recordResult(self, score: str, winner: Participant):
        """Records the final score and sets the winning participant."""
        self.__score = score
        self.__winner = winner

    def getWinner(self) -> Participant:
        """Returns the winning Participant object."""
        return self.__winner

    def get_details(self) -> str:
        """Helper method to display match information."""
        p1_name = self.__participant1.get_name() if self.__participant1 else "TBD"
        p2_name = self.__participant2.get_name() if self.__participant2 else "TBD"
        winner_name = self.__winner.get_name() if self.__winner else "Pending"
        
        return f"Match {self.__id}: {p1_name} vs {p2_name} | Score: {self.__score} | Winner: {winner_name}"