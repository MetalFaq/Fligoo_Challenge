# This file contains reusable functions to interact with de data in the database. 
# Create, read, update and delete (CRUD). 
import json
from sqlalchemy.orm import Session

from . import models, schemas

# Here are created funtions that will manipulate the data on the model "Game"
class GameRepo:

    def create(db: Session, game: schemas.GameCreate):
        try: 
            db_game = models.Game(
                # Can access from index
                player1 = json.dumps([game.player1.name, game.player1.symbol]),
                player2 = json.dumps([game.player2.name, game.player2.symbol]),
                movements_played = 0,
                next_turn = game.player1.name, # The first registered player starts
                board = json.dumps([[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]),
                
                )
            db.add(db_game)
            db.commit()
            db.refresh(db_game)
            return db_game
        except:
            return ("Validation error")

    def update(db: Session, game_actualizado):
        updated_game = db.merge(game_actualizado)
        db.commit()
        return updated_game   
    
    # If one million games exist, only the first 100 will be returned
    def find_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Game).offset(skip).limit(limit).all()
    
    def find_by_id(db: Session, _id):
        return db.query(models.Game).filter(models.Game.id == _id).first()

    def delete(db: Session, game_id):
        #A database query is a request to access data from a database to manipulate it or retrieve it.
        db_game = db.query(models.Game).filter_by(id=game_id).first() 
        db.delete(db_game)
        db.commit()