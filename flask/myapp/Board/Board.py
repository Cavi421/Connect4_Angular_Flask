# import numpy as np
from Player.Player import PlayerClass
from Utility.Utility import UtilityClass


class BoardClass:
    def __init__(self: object, matrix_board) -> None:
        # Generate the 6x7 matrix using nested list comprehension
        # instead of hard coding it
        #self.UpdateBoard()

        self.matrix_board = matrix_board



    def AddToken(self: object, choosen_column: int, player: PlayerClass) -> tuple:
        """
        Add a token inside the matrix.
        Determine the appropriate placement for the token.
        Return the coordinates in a tuple.
        """

        empty_position_row_id = self.ComputeTokenPosition(choosen_column)

        self.matrix_board[empty_position_row_id][choosen_column] = player.id

        # Return the token coordinates inside the matrix. ex. (1,2) mean row index 1 and column index 2
        msg = "Success: Token Placed on the board"
        return (True, msg, (empty_position_row_id, choosen_column))

    def ComputeTokenPosition(self: object, choosen_column: int):
        """
        When adding a token this function check where is the correct position in the matrix
        to place the token(it can't float around, it needs to have another token below or being at row 0)
        """
        Utility = UtilityClass()

        empty_position_row_id = Utility.ScanMatrixColumnForEmptyPositionId(
            choosen_column, self
        )

        # Insert additional checks here
        return empty_position_row_id
