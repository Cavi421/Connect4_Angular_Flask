import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-connect4',
  templateUrl: './connect4.component.html',
  styleUrls: ['./connect4.component.css'],
})
export class Connect4Component implements OnInit {
  matrix_board: number[][] = [];
  data_form = { answer: '1' }; //default column choice
  msg_to_show = '';
  show_button: boolean = true;

  //Used to add tokens inside the gameboard
  tokens_to_add: any[] = [];

  //Used to mark winning tokens
  winning_tokens: any[] = [];

  constructor(private http: HttpClient) {}

  //Fill Matrix
  ngOnInit(): void {
    for (let row = 0; row < 6; row++) {
      this.matrix_board.push([]);

      for (let column = 0; column < 7; column++) {
        this.matrix_board[row].push(0);
      }
    }
  }

  //SEND REQUESTS METHOD
  sendPostRequest(url: string, data: any) {
    return this.http.post(url, data);
  }

  //Send requests when the button is pressed
  //This sends the state of che current matrix and the answer
  //There is no check for the matrix so a player could send a modified one altering the game
  //Could be a better idea to store the matrix on a DB so also the state is preserved
  onSubmit() {
    let api_url: string = 'http://localhost:5000';
    let post_data: any = {
      data: { answer: this.data_form.answer },
      matrix_board: this.matrix_board,
    };

    //SEND REQUEST TO FLASK
    this.sendPostRequest(api_url, post_data).subscribe({
      next: (response) => this.parseSuccess(response),
      error: (e) => console.error(e),
    });
  }

  parseSuccess(response: any): boolean {
    let human_move_result: boolean = this.parseHumanMove(response);

    //If human move result is false it means:
    //Invalid move, then the user will need to re-submit another choice
    //Game is finished so it's pointeless to execute the AI check
    if (human_move_result == false) {
      return false;
    }

    let ai_move_result: boolean = this.parseAIMove(response);

    if (ai_move_result == false) {
      return false;
    }

    return true;
  }

  //Check if the human move is correct and returns errors in case
  parseHumanMove(response: any): boolean {
    //Stores json response into variables
    let human_reponse: any = response['human'];
    let human_last_move_column: number = human_reponse['last_move'][1];
    let human_last_move_row: number = human_reponse['last_move'][0];
    let human_result: boolean = human_reponse['result'];
    let human_msg: string = human_reponse['msg'];
    let human_matrix_board: number[][] = human_reponse['matrix_board'];
    let human_token_id: number = human_reponse['token_id'];

    //Check if flask returned any error, e.g. column is full
    if (human_result == false) {
      console.log(human_msg);
      this.msg_to_show = human_msg;
      return false;
    }

    //Update board
    this.matrix_board = human_reponse['matrix_board'];

    //Calculate token's left,top position in pixels
    let position_left: number, position_top: number;
    [position_left, position_top] = this.calculateTokenPositionsCSS(
      human_last_move_row,
      human_last_move_column,
      31,
      32
    );

    //Add tokens to array. This array will be shown in the html template
    let token_to_add = {
      color: 'yellow',
      column: human_last_move_column,
      row: human_last_move_row,
      token_id: human_token_id,
      position_left: position_left + 'px',
      position_top: position_top + 'px',
    };

    //Update msg and add token to the board
    this.tokens_to_add.push(token_to_add);
    this.msg_to_show = human_msg;

    //If game is won by player 1 or game is draw then destroy the submit button to stop the game
    if (this.checkIfGameWonOrDraw(response, 'human') == false) {
      return false;
    }

    //If all the other conditions pass then it's AI turn, otherwise game is finished or player
    //inserted a bad input
    return true;
  }

  parseAIMove(response: any): boolean {
    //Json response stored in variables
    let ai_response: any = response['ai'];
    let ai_last_move_column: number = ai_response['last_move'][1];
    let ai_last_move_row: number = ai_response['last_move'][0];
    let ai_result: boolean = ai_response['result'];
    let ai_msg: string = ai_response['msg'];
    let ai_matrix_board: number[][] = ai_response['matrix_board'];
    let ai_token_id: number = ai_response['token_id'];

    //console.log(ai_msg, ai_result, ai_matrix_board, ai_last_move_row, ai_last_move_column)

    //Update the matrix with the AI move
    this.matrix_board = ai_matrix_board;

    //Calculate token's left,top position in pixels
    let position_left: number, position_top: number;
    [position_left, position_top] = this.calculateTokenPositionsCSS(
      ai_last_move_row,
      ai_last_move_column,
      31, //Starting margin
      32 //Starting margin
    );

    let token_to_add_ai = {
      color: 'red',
      column: ai_last_move_column,
      row: ai_last_move_row,
      token_id: ai_token_id,
      position_left: position_left + 'px',
      position_top: position_top + 'px',
    };

    this.tokens_to_add.push(token_to_add_ai);

    //If game is won by player 1 or game is draw then destroy the submit button to stop the game
    if (this.checkIfGameWonOrDraw(response, 'ai') == false) {
      return false;
    }

    return true;
  }

  //Calculate the css top and left margin used to place the tokens inside the gameboard
  calculateTokenPositionsCSS(
    last_move_row: number,
    last_move_column: number,
    starting_margin_top: number,
    starting_margin_left: number
  ): number[] {
    //Create CSS style rules to position the tokens
    let position_left: number = starting_margin_top + last_move_column * 87;
    let position_top: number = starting_margin_left + last_move_row * 87;

    return [position_left, position_top];
  }

  //If game is won or draw, make the button disappear
  checkIfGameWonOrDraw(response: any, human_or_ai: string): boolean {
    if (
      response[human_or_ai]['is_game_draw'] == true ||
      response[human_or_ai]['is_game_won'] == true
    ) {
      this.show_button = false;
      this.msg_to_show = response[human_or_ai]['msg'];
      this.colorWinningTokens(response[human_or_ai]['winning_cells']);
      return false;
    }

    return true;
  }

  // Marks the winning tokens taking
  colorWinningTokens(cells_array: number[][]): void {
    //Loop through winning cells
    cells_array.forEach((cell) => {
      let row: number = cell[0];
      let column: number = cell[1];

      //Calculate the positions in pixels to mark the winning token
      let position_left: number, position_top: number;
      [position_left, position_top] = this.calculateTokenPositionsCSS(
        row,
        column,
        50,
        48
      );

      // Add winning token to an array that will be looped in the html template
      let winning_token = {
        //"row": row,
        //"column": column,
        position_left: position_left + 'px',
        position_top: position_top + 'px',
      };

      this.winning_tokens.push(winning_token);
    });
  }
}
