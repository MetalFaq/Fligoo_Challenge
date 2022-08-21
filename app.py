#Main application. 
##########################
from queue import Empty
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import json

import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import GameRepo
from config.session import engine, get_db

models.Base.metadata.create_all(bind=engine) #Union between the tables and the DB. 
#API definition
app = FastAPI()

#Swagger
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# Create a game
@app.post('/newgame')
def new_game(game_request: schemas.GameCreate, db: Session = Depends(get_db)):
    #logica para asignar al jugador que va a ir primero. 
    #models.Game.next_turn = game_request.starting_player
    return GameRepo.create(db, game = game_request)

# Submit a play
@app.post('/submitplay')
def submit_play(move_request: schemas.Move, db: Session = Depends(get_db)):

    #Dimension validation
    if move_request.column not in (1, 2, 3):
        return "Error: Dimension Error"
    if move_request.row not in (1, 2, 3):
        return "Error: Dimension Error"
    
    id = move_request.game_id
    juego = GameRepo.find_by_id(db, id)

    if juego:       

        # Deserialize player's info. 
        p1 = json.loads(juego.player1) #p[0]:name, p[1]:symbol
        p2 = json.loads(juego.player2)

        # Symbol validation
        if(p1[1] == p2[1]):
            return "Error: Same Symbol with other player"
        # Name validation
        if move_request.player not in (p1[0], p2[0]):
            return "Error: Name not found."

        #if juego.next_turn not in (p1[0], p2[0]):
        #   return "Error: Starting player not found."
        
        # Starting player validation. Not two plays of the same player allowed!
        if juego.next_turn != move_request.player:
            return "Error: It's not your turn."
        
        # Insert logic here!.
        current_player = None
        next_player = None
        #current winner = None

        if(p1[0] == move_request.player):
            current_player = p1
            next_player = p2
        else:
            current_player = p2
            next_player = p1   

        # Deserealize table
        new_board = json.loads(juego.board)
        # Symbol is assigned in the table
        new_board[move_request.row - 1][move_request.column - 1]=current_player[1]
        
        # No deberia poder jugar sobre un punto ya ocupado por un signo
        # if new_board[move_request.row - 1][move_request.column - 1] :
        #     new_board[move_request.row - 1][move_request.column - 1] = current_player[1] 
        # else:
        #     return "Error: Point already taken" 
        
        move_played = models.Game(
            id = juego.id,
            movements_played = juego.movements_played + 1,
            next_turn = next_player[0],
            board = json.dumps(new_board),
            player1 = json.dumps(p1),
            player2 = json.dumps(p2),
            winner = "None" #current winner: None or p1/2[0]
        )
        GameRepo.update(db, move_played)
        
        return GameRepo.find_by_id(db, juego.id)
    else:
        raise HTTPException(status_code=404, detail="Error: The game doesn't exist.")

# List all games.
@app.get('/all_games')
def get_games(db: Session = Depends(get_db)):

    games = GameRepo.find_all(db)
    if games:
        return games
    raise HTTPException(status_code=400, detail="Error: None game was founded") #bad sintaxis


# Retrieve a single game
@app.get('/get_game/{id_game}')
def get_game(id_game: int,db: Session = Depends(get_db)):

    game = GameRepo.find_by_id(db, id_game)    
    if game:
        return game
    raise HTTPException(status_code=404, detail="Error: None game was founded")

# Delete a game
@app.delete('/delete_game/{id_game}')
def delete_game(id_game: int, db: Session = Depends(get_db)):

    game = GameRepo.find_by_id(db, id_game)

    if game is None:
        raise HTTPException(status_code=404, detail="Error: Game doesn't exist or alredy eliminated")

    GameRepo.delete(db, id_game)
    return "Game deleted"

# Start of the API / Setup the Web Server
# host= "0.0.0.0": Listen all TCP traffic
# port: endpoint of a network connection between the web server and a web client
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

##########################################################

# Improves: 
# Endpoint ---> "Create a game"#      
#       * Let the players choose who goes first.
# Endpoint ---> "Submit a play"
#       * If a table point is already occupied by a symbol, you cannot overwrite it.
#       * What happens if there are no more moves? Tie!
#       * How do you know there is a winner before or after a move?
# Endpoint ---> "List all games"
#       * Filter: Finished & Unfinished games (state of the board)
# General
#       * Modular el programa: apiRoute(), llamar funciones de lógica de otros archivos...
