# Pydantic parse and validate data
# It provides user-friendly errors, allowing to catch any invalid data. 
from pydantic import BaseModel, validator

# PLAYER SCHEMA

class Player(BaseModel):

    name: str
    symbol: str

    @validator('symbol')
    def lenght_symbol(cls, value):
        if len(value)>1:
            raise ValueError("Max Lenght for symbol = 1")
        if len(value) < 1:
            raise ValueError("Error symbol")

    @validator('name')
    def lenght_name(cls, value):
        if len(value)>50:
            raise ValueError("Max Lenght for name = 50")
        if len(value) < 1:
            raise ValueError("Error name")


# GAME SCHEMA

class GameBase(BaseModel):

    player1: Player
    player2: Player   
            
         
# GameCreate hereda de GameBase sus atributos
class GameCreate(GameBase):
    pass


class Game(GameBase):

    id: int
    movements_played: int
    next_turn: str
    board: str

    # permite el mapeo con el models Game
    class Config:
        orm_mode = True

# MOVEMENT SCHEMA

class Move(BaseModel):
    game_id: int
    player: str
    row: int
    column: int

    