import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-hello-world',
  templateUrl: './hello-world.component.html',
  styleUrls: ['./hello-world.component.css'],
})
export class HelloWorldComponent implements OnInit {
  matrix_board: number[][] = [];
  data_form = { answer: '1' };
  msg_to_show = '';
  show_button: boolean = true;

  //Token
  tokens_to_add: any[] = [];

  // 
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
  sendPostRequest(url: string, data: any): Observable<Object> {
    return this.http.post(url, data);
  }

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
      complete: () => console.info('complete'),
    });
  }


  parseSuccess(response: any): boolean {
    let human_move_result: boolean = this.parseHumanMove(response);

    //If human move reuslt is false it means:
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

    //Create CSS style rules to position the tokens
    let position_left: number = 31 + human_last_move_column * 87;
    let position_top: number = 32 + human_last_move_row * 87;

    //Add tokens to array. This array will be shown in the html template
    let token_to_add = {
      color: 'yellow',
      column: human_last_move_column,
      row: human_last_move_row,
      token_id: human_token_id,
      position_left: position_left + 'px',
      position_top: position_top + 'px',
    };

    this.tokens_to_add.push(token_to_add);
    this.msg_to_show = human_msg;

    //If game is won by player 1 or game is draw then destroy the submit button to stop the game
    if (
      response['human']['is_game_draw'] == true ||
      response['human']['is_game_won'] == true
    ) {
      this.show_button = false;
      this.msg_to_show = human_msg
      this.colorWinningTokens(human_reponse["winning_cells"])
      return false;
    }

    return true;
  }

  parseAIMove(response: any): boolean {
    let ai_response = response['ai'];
    let ai_last_move_column: number = ai_response['last_move'][1];
    let ai_last_move_row: number = ai_response['last_move'][0];
    let ai_result: boolean = ai_response['result'];
    let ai_msg: string = ai_response['msg'];
    let ai_matrix_board: number[][] = ai_response['matrix_board'];
    let ai_token_id: number = ai_response['token_id'];


    console.log(ai_msg, ai_result, ai_matrix_board, ai_last_move_row, ai_last_move_column)

    this.matrix_board = ai_matrix_board;

    let position_left_ai = 31 + ai_last_move_column * 87;
    let position_top_ai = 32 + ai_last_move_row * 87;

    let token_to_add_ai = {
      color: 'red',
      column: ai_last_move_column,
      row: ai_last_move_row,
      token_id: ai_token_id,
      position_left: position_left_ai + 'px',
      position_top: position_top_ai + 'px',
    };

    this.tokens_to_add.push(token_to_add_ai);

    if (
      response['ai']['is_game_draw'] == true ||
      response['ai']['is_game_won'] == true
    ) {
      this.show_button = false;
      this.msg_to_show = ai_msg
      this.colorWinningTokens(ai_response["winning_cells"])
      return true;
    }

    return true;
  }




  colorWinningTokens(cells_array: number[][]): void {

    cells_array.forEach(cell => {
      let row = cell[0]
      let column = cell[1]


      let position_left = 48 + column * 87;
      let position_top = 50 + row * 87;


      let winning_token = {
        "row": row,
        "column": column,
        "position_left": position_left + "px",
        "position_top": position_top + "px"
      }

      this.winning_tokens.push(winning_token)

    });

  }

}
