from flask import Flask, render_template, request
from Connect4.Connect4 import Connect4Class
from flask_cors import cross_origin


app = Flask(__name__, template_folder="templates/")


@app.route("/", methods=["POST"])
@cross_origin()
def index():
    if request.method == "POST":
        jsonData = request.get_json()
        # Pass Data to Connect4
        # print(jsonData)

        # Column choosen by the player
        # And current status of the matrix_board
        choosen_column = str(jsonData["data"]["answer"])
        matrix_board = jsonData["matrix_board"]

        Connect4 = Connect4Class(choosen_column, matrix_board)
        data_to_send_back = Connect4.Analyze()

        # print(jsonData)

        return data_to_send_back


# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
