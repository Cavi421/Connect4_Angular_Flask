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

    def InitializeJson(self: object) -> None:
        # Json to send back
        self.data_to_send_back = {}
        self.data_to_send_back["human"] = {}
        self.data_to_send_back["ai"] = {}

        self.data_to_send_back["human"]["matrix_board"] = self.matrix_board
        self.data_to_send_back["human"]["last_move"] = [-1, self.choosen_column]

        # data_to_send_back["human"]["msg"] = ""
        # data_to_send_back["human"]["result"] = False
        # data_to_send_back["human"]["last_move"] = [-1, self.choosen_column]
        # data_to_send_back["human"]["is_game_won"] = False
        # data_to_send_back["human"]["is_game_draw"] = False
        # data_to_send_back["human"]["player_id"] = 1
        # data_to_send_back["human"]["winning_cells"] = []

    def AITurn(self: object) -> None:
        self.random_column = self.player2.ThinkMove(self.Board)

        # Add Token To Board
        is_token_placed, msg, last_move = self.Board.AddToken(
            self.random_column, self.player2
        )

        number_of_zeroes = 0
        for row in self.Board.matrix_board:
            number_of_zeroes += row.count(0)

        self.data_to_send_back["ai"]["token_id"] = 42 - number_of_zeroes

        self.data_to_send_back["ai"]["last_move"] = last_move
        self.data_to_send_back["ai"]["matrix_board"] = self.Board.matrix_board

        # Check win conditions
        is_game_won_by_ai, msg = self.Referee.IsGameWon(
            self.Board, last_move, self.player2
        )
        if is_game_won_by_ai:
            self.data_to_send_back["ai"]["result"] = True
            self.data_to_send_back["ai"]["msg"] = msg
            self.data_to_send_back["ai"]["is_game_won"] = True
            self.data_to_send_back["ai"]["winning_cells"] = self.Referee.winning_cells

    def HumanTurn(self: object) -> bool:
        # Check INPUT from the player
        is_input_int, msg = self.PlayerInputValidator.CheckInput(self.choosen_column)

        # Return input with error message
        if not is_input_int:
            self.data_to_send_back["human"]["msg"] = msg
            self.data_to_send_back["human"]["result"] = is_input_int

            return False

        #####################################

        # Convert input into matrix index
        self.choosen_column = (
            self.PlayerInputValidator.ConvertPlayerInputIntoMatrixInput()
        )

        #####################################

        # Check Move made by the player
        MoveValidator = MoveValidatorClass()
        is_move_correct, msg = MoveValidator.CheckMove(
            self.choosen_column, self.Board, self.player1
        )

        if not is_move_correct:
            self.data_to_send_back["human"]["msg"] = msg
            self.data_to_send_back["human"]["result"] = is_move_correct

            return False

        #####################################

        # Add Token To Board
        is_token_placed, msg, last_move = self.Board.AddToken(
            self.choosen_column, self.player1
        )

        #### TOKEN HAS BEEN PLACED ####

        # Generate Token ID
        number_of_zeroes = 0
        for row in self.Board.matrix_board:
            number_of_zeroes += row.count(0)

        self.data_to_send_back["human"]["token_id"] = 42 - number_of_zeroes
        self.data_to_send_back["human"]["last_move"] = last_move
        self.data_to_send_back["human"]["matrix_board"] = self.Board.matrix_board
        #####################################

        # CHECK WIN CONDITION
        is_game_won_by_human, msg = self.Referee.IsGameWon(
            self.Board, last_move, self.player1
        )
        if is_game_won_by_human:
            self.data_to_send_back["human"]["result"] = True
            self.data_to_send_back["human"]["msg"] = msg
            self.data_to_send_back["human"]["is_game_won"] = True
            self.data_to_send_back["human"][
                "winning_cells"
            ] = self.Referee.winning_cells

            # gamw won, used to stop the ai player
            return False
        #####################################

        # If nothing of the above happened then prepare for the next turn
        self.data_to_send_back["human"]["result"] = True
        self.data_to_send_back["human"]["msg"] = "Select a Column"
        return True

    def Analyze(self: object) -> None:
        #### Instantiates the various classes ####
        # Json to send back
        self.InitializeJson()
        self.Referee = RefereeClass()

        self.player1 = HumanClass(1)
        self.player2 = AIClass(2)

        self.Board = BoardClass(self.matrix_board)
        self.PlayerInputValidator = PlayerInputValidatorClass()
        self.MoveValidator = MoveValidatorClass()

        #### HUMAN PLAYER TURN ####

        # If turn is not successful or game is won by human player
        # returns the json, stopping the AI player
        if not self.HumanTurn():
            return self.data_to_send_back

        #### AI TURN ####
        self.AITurn()

        # Check if the game is a draw
        is_game_draw, msg = self.Referee.IsGameDraw(self.Board)
        if is_game_draw:
            self.data_to_send_back["ai"]["result"] = True
            self.data_to_send_back["ai"]["msg"] = msg
            self.data_to_send_back["ai"]["is_game_draw"] = True

        return self.data_to_send_back
