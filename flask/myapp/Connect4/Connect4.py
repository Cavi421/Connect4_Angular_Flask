from Player.Human import HumanClass
from Validator.PlayerInputValidator import PlayerInputValidatorClass
from Validator.MoveValidator import MoveValidatorClass
from Board.Board import BoardClass
from Referee.Referee import RefereeClass
from Player.AI import AIClass


class Connect4Class:
    def __init__(
        self: object, choosen_column: int, matrix_board: list[list[int]]
    ) -> None:
        self.choosen_column = choosen_column
        self.matrix_board = matrix_board

    def Analyze(self: object) -> None:
        # Json to send back
        data_to_send_back = {}
        data_to_send_back["human"] = {}
        data_to_send_back["ai"] = {}

        data_to_send_back["human"]["msg"] = ""
        data_to_send_back["human"]["result"] = False
        data_to_send_back["human"]["last_move"] = [-1, self.choosen_column]
        data_to_send_back["human"]["matrix_board"] = self.matrix_board
        data_to_send_back["human"]["is_game_won"] = False
        data_to_send_back["human"]["is_game_draw"] = False
        data_to_send_back["human"]["player_id"] = 1
        data_to_send_back["human"]["winning_cells"] = []

        # Human Player Turn
        self.player1 = HumanClass(1)
        Referee = RefereeClass()

        # Instantiate Board class
        Board = BoardClass(self.matrix_board)

        # Check and polish input
        PlayerInputValidator = PlayerInputValidatorClass()
        is_input_int, msg = PlayerInputValidator.CheckInput(self.choosen_column)

        # Return input with error message
        if not is_input_int:
            data_to_send_back["human"]["msg"] = msg
            data_to_send_back["human"]["result"] = is_input_int

            return data_to_send_back

        # Convert input into matrix index
        self.choosen_column = PlayerInputValidator.ConvertPlayerInputIntoMatrixInput()

        # Validate Move
        MoveValidator = MoveValidatorClass()
        is_move_correct, msg = MoveValidator.CheckMove(
            self.choosen_column, Board, self.player1
        )

        if not is_move_correct:
            data_to_send_back["human"]["msg"] = msg
            data_to_send_back["human"]["result"] = is_move_correct

            return data_to_send_back

        # Add Token To Board
        is_token_placed, msg, last_move = Board.AddToken(
            self.choosen_column, self.player1
        )

        #### TOKEN PLACED ####

        number_of_zeroes = 0
        for row in Board.matrix_board:
            number_of_zeroes += row.count(0)

        data_to_send_back["human"]["token_id"] = 42 - number_of_zeroes

        data_to_send_back["human"]["last_move"] = last_move
        data_to_send_back["human"]["matrix_board"] = Board.matrix_board

        # Check win conditions

        is_game_won_by_human, msg = Referee.IsGameWon(Board, last_move, self.player1)
        if is_game_won_by_human:
            data_to_send_back["human"]["result"] = True
            data_to_send_back["human"]["msg"] = msg
            data_to_send_back["human"]["is_game_won"] = True
            data_to_send_back["human"]["winning_cells"] = Referee.winning_cells
            return data_to_send_back

        data_to_send_back["human"]["result"] = True
        data_to_send_back["human"]["msg"] = "Select a Column"

        #### AI TURN ####
        self.player2 = AIClass(2)

        # print(Board.matrix_board)

        self.random_column = self.player2.ThinkMove(Board)

        print("self_random_column", self.random_column)

        # Add Token To Board
        is_token_placed, msg, last_move = Board.AddToken(
            self.random_column, self.player2
        )

        number_of_zeroes = 0
        for row in Board.matrix_board:
            number_of_zeroes += row.count(0)

        data_to_send_back["ai"]["token_id"] = 42 - number_of_zeroes

        data_to_send_back["ai"]["last_move"] = last_move
        data_to_send_back["ai"]["matrix_board"] = Board.matrix_board

        print("self_last_move", last_move)

        # Check win conditions
        is_game_won_by_ai, msg = Referee.IsGameWon(Board, last_move, self.player2)
        if is_game_won_by_ai:
            data_to_send_back["ai"]["result"] = True
            data_to_send_back["ai"]["msg"] = msg
            data_to_send_back["ai"]["is_game_won"] = True
            data_to_send_back["ai"]["winning_cells"] = Referee.winning_cells
            return data_to_send_back

        # Check if the game is a draw
        is_game_draw, msg = Referee.IsGameDraw(Board)
        if is_game_draw:
            data_to_send_back["ai"]["result"] = True
            data_to_send_back["ai"]["msg"] = msg
            data_to_send_back["ai"]["is_game_draw"] = True

            return data_to_send_back

        data_to_send_back["ai"]["result"] = True
        data_to_send_back["ai"]["msg"] = "Select a Column"

        return data_to_send_back
