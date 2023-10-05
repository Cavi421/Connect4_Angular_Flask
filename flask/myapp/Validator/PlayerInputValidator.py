from Board.Board import BoardClass
from Validator.Validator import ValidatorClass


class PlayerInputValidatorClass(ValidatorClass):
    """
    This class will perform a series of sanity checks to make sure
    that the human's player input is an INT between 1 and 7
    If not returns False and the method which called this one
    will keep looping.
    """

    def CheckInput(self, player_input: int) -> bool:
        self.choosen_column = player_input

        result, msg = self.IsNotEmpty()
        if not result:
            return (False, msg)

        result, msg = self.IsInt()
        if not result:
            return (False, msg)

        result, msg = self.IsPositiveInt()
        if not result:
            return (False, msg)

        result, msg = self.IsChoosenColumnInBound()
        if not result:
            return (False, msg)

        # If all the checks pass then return True
        msg = "Player input is INT"
        return (True, msg)


    def ConvertPlayerInputIntoMatrixInput(self) -> int:
        
        self.choosen_column -= 1
        return self.choosen_column


    def IsNotEmpty(self) -> bool:
        if self.choosen_column == "":
            msg = "Warning: Choose value is empty, try again"
            #print(msg)
            return (False, msg)

        else:
            return (True, "Success: Value is not empty")

    def IsInt(self) -> bool:
        """
        isdigit returns True if it's an integer.
        Doesn't work with neg integers.
        Using isdigit because if you use int() on a
        string that represents a float if gets truncated
        e.g. "1.2" becomes 1
        """

        # Signed integers
        if self.choosen_column[0] in ["+", "-"]:
            # Don't consider the first letter of the string + or -
            if self.choosen_column[1:].isdigit():
                self.choosen_column = int(self.choosen_column)
                return (True, "Success: Value is INT")

            else:
                
                msg = "Warning: Input choosen is not an Integer number, try again"
                #print("Warning: Input choosen is not an Integer number, try again")
                return (False, msg)

        # Unsigned integers
        else:
            if self.choosen_column.isdigit():
                self.choosen_column = int(self.choosen_column)
                return (True, "Success: Value is INT")

            else:
                #print("Warning: Input choosen is not an Integer number, try again")
                msg = ("Warning: Input choosen is not an Integer number, try again")
                return (False, msg)

    def IsPositiveInt(self) -> bool:
        if self.choosen_column < 0:

            msg = "Warning: Column number can't be negative, try again"
            #print(msg)
            return (False, msg)

        else:
            msg = "Success: INT is positive"
            return (True, msg)

    def IsChoosenColumnInBound(self) -> bool:
        if self.choosen_column <= 0 or self.choosen_column >= 8:
            
            msg = "Warning: Wrong column number,it should be between 1 and 7"
            #print(msg)
            return (False, msg)

        else:
            msg = "Success: Column is in bound"
            return (True, msg)
