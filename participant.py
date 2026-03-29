from abc import ABC, abstractmethod

class Participant(ABC):
    def __init__(self, participant_id: int, name: str):
        """
        Initializes the Participant with private attributes to ensure encapsulation.
        """
        self.__id = participant_id
        self.__name = name

    def get_name(self) -> str:
        """
        Public method to access the private name attribute.
        """
        return self.__name
    
    def get_id(self) -> int:
        """
        Public method to access the private id attribute.
        """
        return self.__id

    @abstractmethod
    def register(self) -> str:
        """
        Abstract method representing the registration process.
        Any class inheriting from Participant MUST implement this method.
        """
        pass