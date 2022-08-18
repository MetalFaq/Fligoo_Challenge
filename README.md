# Tic-Tac-Toe API
The goal of the project is to develop an API that lets you play the tic-tac-toe game.

## Assigments
"The goal of this exercise is to develop an API that lets you play the tic-tac-toe game,
validate the board and return the winner, a message saying it was a tie, or an error if 
there was some kind of problem with the input data."

## Features
<ul>
<li>
  Provide an endpoint that will receive the info of two players. <br>
  In response, the API will return an object with the game ID, player info and which player has to play next.
  </li>
<li>
  When a game is created, the player who goes next should be able to submit a move.<br>
  In order to do that, another endpoint expects the game id, player name, row, and column. <br>
  The returned data should be the board state after the current play.<br>
  If the last move causes the game to end, the name of the winner should be on the "winner" field.
  </li>
<li>
  Provide an endpoint to list all the games. Finished games should also specify the winner.  
  </li>
<li>
  The API should let the user retrieve a single game by its ID.
  </li>
<li>
  Provide a way to delete a game by ID.
  </li>
</ul>

### Tech
<ul>
<li>Python - high-level programming language.</li>
<li>fastAPI - high-performance web framework for building APIs.</li>
<li>SQLAlchemy - Python SQL toolkit and Object Relational Mapper (ORM)</li>
<li>SQLite - DB Engine.</li>
</ul>

### Installation 
This app requires Python 3.10 to run
<ul>
<li>
Git Clone (INSERTAR LINK DEL REPO)
</li>
<li>
Install the dependencies from requirements.txt by creating and activating a
new virtual environment. (INSERTAR CÓDIGO)
</li> 
</ul>

### Running the app
INSERTAR COMANDOS. 
