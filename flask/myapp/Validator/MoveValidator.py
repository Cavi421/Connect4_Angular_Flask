from Board.Board import BoardClass
from Validator.Validator import ValidatorClass
from Utility.Utility import UtilityClass
from Player.Player import PlayerClass

class MoveValidatorClass(ValidatorClass):
    """
    This class will perform a series of checks:
    - Check if the move is valid (e.g., if the column is not full)
    """


    def CheckMove(self, column_choosen: int, Board: BoardClass, player: PlayerClass) -> bool:
        
        #Return true if column is not full, otheriwse false
        if not self.CheckIfColumnIsNotFull(column_choosen, Board):
            
            msg = "Warning: This column is full, try again"
            #Otherwise when it's the AI turn it keeps spamming until it chooses a valid column
            if not player.isAI:
                print(msg)
                
            return (False, msg)
        
        
        msg = "Success: Column has an available spot"
        return (True, msg)



    def CheckIfColumnIsNotFull(self, column_choosen, Board: BoardClass) -> bool:
        """
        Check if the column is not full using one of the Utility methods
        """

        Utility = UtilityClass()

        if Utility.ScanMatrixColumnToSeeIfIsNotFull(column_choosen, Board) == False:
            return False
        
        return True
            