from participant import Participant
from player import Player

class Team(Participant):
    def __init__(self, participant_id: int, name: str):
        super().__init__(participant_id, name)
        
        # Encapsulated specific attribute: a list to hold Player objects
        self.__player_list = []

    def addPlayer(self, player: Player):
        """Adds a Player object to the team's roster."""
        self.__player_list.append(player)

    def showTeam(self) -> str:
        """Returns a string representation of the team and its players."""
        if not self.__player_list:
            return f"Team '{self.get_name()}' currently has no players."
            
        team_info = f"Team '{self.get_name()}' Roster:\n"
        for player in self.__player_list:
            team_info += f" - {player.get_name()} ('{player.get_nickname()}')\n"
        return team_info

    # We MUST implement the abstract method from Participant
    def register(self) -> str:
        return f"Team registered: {self.get_name()} with {len(self.__player_list)} players."