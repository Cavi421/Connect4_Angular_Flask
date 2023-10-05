import abc

class PlayerClass(abc.ABC):
    """
    Interface for the PlayerClass
    """

    def __init__(self:object , player_id: int) -> None:
        self.id = player_id
        self.SetName()
        self.SetIfAI()

    @abc.abstractmethod
    def ThinkMove(self:object) -> int:
        pass

    
    @abc.abstractmethod
    def SetName(self:object) -> None:
        pass