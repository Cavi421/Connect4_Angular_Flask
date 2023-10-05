class UtilityClass:
    def ScanMatrixColumnForEmptyPositionId(
        self: object, choosen_column: int, Board: object
    ) -> int:
        """
        Given a column, this method scans it and return the first empty position as row_index
        """
        # Scan every row and then the specific column
        # The numbers inserted inside range are for scanning in reversed order, starting from the bottom
        for row_index in range(5, -1, -1):

            #print(row_index, choosen_column)

            # Token can be added because there is an empty slot
            if Board.matrix_board[row_index][choosen_column] == 0:
                return row_index


        #Return -1 if there are no empty positions, it shouldn't happen though considering previous checks
        return -1
        

    def ScanMatrixColumnToSeeIfIsNotFull(
        self: object, choosen_column: int, Board: object
    ) -> bool:
        """
        Scan the column to check if there is at least one ZERO.
        In this case the column is not full
        """

        #print(Board.matrix_board)

        # Scan every row and then the specific column
        for row_index in range(0, 6):

            # Token can be added because there is an empty slot
            if Board.matrix_board[row_index][choosen_column] == 0:
                return True

        return False
