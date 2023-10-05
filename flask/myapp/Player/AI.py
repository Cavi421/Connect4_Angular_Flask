from Player.Player import PlayerClass
from Board.Board import BoardClass
from Validator.MoveValidator import MoveValidatorClass
from random import randint


class AIClass(PlayerClass):
    def SetName(self: object) -> None:
        self.name = f"AI"

    def SetIfAI(self: object) -> None:
        self.isAI = True

    def ThinkMove(self: object, Board: BoardClass) -> int:
        """
        Method used to simulate the "thinking process".
        Returns the column chosen by the algorithm.
        """

        random_column = self.AICalculateRandomPositionToAddToken(Board)

        return random_column

    def AICalculateRandomPositionToAddToken(self: object, Board: BoardClass) -> int:
        """
        Choose a random column where to place the token
        and then test if the column is valid (if the token can be added there).
        """

        MoveValidator = MoveValidatorClass()

        is_move_valid = False
        while not is_move_valid:
            random_column = randint(0, 6)

            is_move_valid, msg = MoveValidator.CheckMove(random_column, Board, self)

        return random_column
