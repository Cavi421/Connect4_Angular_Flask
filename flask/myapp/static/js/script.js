//const btn = document.querySelector('.send__data__btn');
var board = document.getElementById("game-table");
var info_msg = document.getElementById("info_msg");

//Instantiates Matrix Board
let matrix_board = []
for (let row = 0; row < 6; row++) {
    matrix_board.push([])

    for (let column = 0; column < 7; column++) {
        matrix_board[row].push(0);
    }
}



document.getElementById('column_form').addEventListener('submit', function (event) {
    event.preventDefault();


    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ data, "matrix_board": matrix_board })
    })
        .then(response => response.json())
        .then(data => {


            //PLAYER
            matrix_board = data["human"]["matrix_board"]
            msg = data["human"]["msg"]
            console.log('Success:', data);

            // add disc
            disc_color = "yellow"
            if (data["human"]["player_id"] == 1) {
                disc_color = "red"
            }

            
            id = data["human"]["token_id"]

            column_choosen = data["human"]["last_move"][1]
            row_choosen = data["human"]["last_move"][0]



            board.innerHTML += '<div id="d'+id+'" class="disc '+ disc_color +'"></div>'
            document.getElementById('d'+id).style.left = (31+ 87*column_choosen)+"px";
            document.getElementById('d'+id).style.top = (32+ 87*row_choosen)+"px";
            info_msg.innerHTML = msg



            if (data["human"]["is_game_draw"] == true || data["human"]["is_game_won"] == true) {
                document.getElementById("submit_button").remove()
            }




            //AI ADD DISC

            matrix_board = data["ai"]["matrix_board"]
            console.log('Success:', data);

            // add disc
            disc_color = "yellow"
            if (data["ai"]["player_id"] == 1) {
                disc_color = "red"
            }

            
            id = data["ai"]["token_id"]

            column_choosen = data["ai"]["last_move"][1]
            row_choosen = data["ai"]["last_move"][0]



            board.innerHTML += '<div id="d'+id+'" class="disc '+ disc_color +'"></div>'
            document.getElementById('d'+id).style.left = (31+ 87*column_choosen)+"px";
            document.getElementById('d'+id).style.top = (32+ 87*row_choosen)+"px";



            if (data["ai"]["is_game_draw"] == true || data["ai"]["is_game_won"] == true) {
                document.getElementById("submit_button").remove()
            }


        })
        .catch(error => {
            console.error('Error:', error);
        });
});
