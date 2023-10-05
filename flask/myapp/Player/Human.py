from Player.Player import PlayerClass
from Board.Board import BoardClass
from Validator.PlayerInputValidator import PlayerInputValidatorClass
from Validator.MoveValidator import MoveValidatorClass


class HumanClass(PlayerClass):
    def SetName(self:object) -> None:
        self.name = f"Player n{self.id}"
        self.d_tokens = {
            1: "O",
            2: "X"
        }

    def SetIfAI(self:object) -> None:
        self.isAI = False

    def ThinkMove(self:object, Board: BoardClass) -> int:
        """
        This method prompts the user to choose a column repeatedly until a valid choice is made.
        It will keep asking until the user's input is correct and the move is considered valid.
        Return the choosen column which has been polished and validated.
        """

        PlayerInputValidator = PlayerInputValidatorClass()

        is_input_correct = False
        is_move_correct = False

        #If both the input and the move are correct, the loop is considered finished.
        while not is_input_correct or not is_move_correct:
            self.choosen_column = input(
                f"SELECT a column number where to place the Token '{self.d_tokens[self.id]}': "
            )

            # Check if the inuput is an INT
            is_input_correct = PlayerInputValidator.CheckInput(self.choosen_column)

            if not is_input_correct:
                continue

            # Converted column, taken directly from the validator object
            self.choosen_column = int(self.choosen_column)

            # This is to facilitate users, numbering the columns from 1 to 7
            # In reality matrices work with indices from 0 to 6
            # So this line is to convert from a human-readable index to the matrix's one
            self.choosen_column -= 1

            #### VALIDATE IF A MOVE IS VALID using Validator ####
            MoveValidator = MoveValidatorClass()
            is_move_correct = MoveValidator.CheckMove(self.choosen_column, Board, self)

        return self.choosen_column
