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

models.Base.metadata.create_all(bind=engine) #Create all tables. 
#API definition
app = FastAPI(title = "Tic Tac Toe", description="Challenge from Fligoo")

#Swagger
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# Create a game
@app.post('/newgame', response_model=schemas.GameCreate)
def new_game(game_request: schemas.GameCreate, db: Session = Depends(get_db)):
    
    # Symbol validation
    if game_request.player1.symbol == game_request.player2.symbol:        
        return "Error: Same Symbol"
    # Names validation
    if game_request.player1.name == game_request.player2.name:
        return "Error: Must be different name"
    if game_request.starting_player != game_request.player1.name and game_request.starting_player != game_request.player2.name:
        return "Error: Unregistered name."
    
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
        
        if juego.winner != None:
            return "Error: Finished game"

        # Deserialize player's info. 
        p1 = json.loads(juego.player1) #p[0]:name, p[1]:symbol
        p2 = json.loads(juego.player2)        
       
        # Name validation        
        if move_request.player not in (p1[0], p2[0]):
            return "Error: Name not found." 
        # Starting player validation. Not two plays of the same player allowed!
        if juego.next_turn != move_request.player:
            return "Error: It's not your turn."
        
        # Insert logic here!.
        
        current_player = None
        next_player = None
        current_winner = None

        if(p1[0] == move_request.player):
            current_player = p1
            next_player = p2
        else:
            current_player = p2
            next_player = p1   

        # Deserealize table
        new_board = json.loads(juego.board)
        # Symbol is assigned in the table.  
        if new_board[move_request.row - 1][move_request.column - 1] == " " :
            new_board[move_request.row - 1][move_request.column - 1] = current_player[1] 
        else:
            return "Error: Point already taken" 

        total_movements = juego.movements_played + 1             
                
        move_played = models.Game(
            id = juego.id,
            movements_played = total_movements,
            next_turn = next_player[0],
            board = json.dumps(new_board),
            player1 = json.dumps(p1),
            player2 = json.dumps(p2),
            winner = current_winner #current winner: None or p1/2[0]
        )
        GameRepo.update(db, move_played)
        
        result = isWinner(new_board, p1, p2)
        if result:
            move_played.winner = result[0]
            GameRepo.update(db, move_played)
            return "Winner is " + result[0]
        
        # This conditional check if the board is full
        if total_movements == 9:
            move_played.winner = "No winner"
            GameRepo.update(db, move_played)
            return "IT'S A TIE!" 

        return GameRepo.find_by_id(db, juego.id)
    else:
        raise HTTPException(status_code=404, detail="Error: The game doesn't exist.")

# List all games.
# /{winner} optional. 
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

def isWinner(board, p1, p2):    
    # Check the rows
    for row in range (0, 2):
        if (board[row][0] == board[row][1] == board[row][2] == p1[1]):            
            return p1
   
        elif (board[row][0] == board[row][1] == board[row][2] == p2[1]):            
            return p2

    # Check the columns
    for col in range (0, 2):
        if (board[0][col] == board[1][col] == board[2][col] == p1[1]):            
            return p1

        elif (board[0][col] == board[1][col] == board[2][col] == p2[1]):            
            return p2

    # Check the diagnoals
    if board[0][0] == board[1][1] == board[2][2] == p1[1]:        
        return p1

    elif board[0][0] == board[1][1] == board[2][2] == p2[1]:
        return p2

    elif board[0][2] == board[1][1] == board[2][0] == p1[1]:        
        return p1

    elif board[0][2] == board[1][1] == board[2][0] == p2[1]:       
        return p2

    return False

# Setup the Web Server
# host= "0.0.0.0": Listen all TCP traffic
# port: endpoint of a network connection between the web server and a web client
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

##########################################################

# Improves: 
# Endpoint ---> "List all games"
#       * Filter: Finished & Unfinished games (state of the board)
# General
#       * Modular el programa: apiRoute(), llamar funciones de lógica de otros archivos...