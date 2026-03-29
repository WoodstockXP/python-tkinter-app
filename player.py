from participant import Participant

class Player(Participant):
    def __init__(self, participant_id: int, name: str, nickname: str, ranking: int):
        # Call the constructor of the parent class (Participant)
        super().__init__(participant_id, name)
        
        # Encapsulated specific attributes for Player
        self.__nickname = nickname
        self.__ranking = ranking

    def get_nickname(self) -> str:
        return self.__nickname

    def get_ranking(self) -> int:
        return self.__ranking

    def set_ranking(self, new_ranking: int):
        self.__ranking = new_ranking

    def playMatch(self) -> str:
        """Method specified in the UML/Class design."""
        return f"Player {self.get_name()} ('{self.__nickname}') is ready to play!"

    # Implements the abstract method from Participant
    def register(self) -> str:
        return f"Player registered: {self.get_name()} (Rank: {self.__ranking})"