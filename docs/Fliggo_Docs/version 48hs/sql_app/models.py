# These Pydantic models define more or less a valid data shape
from sqlalchemy import Column, Integer, String
from config.session import Base

# nullable = True/False. The value depends on whether Null values ​​are needed or not. 
# Single tabla needed
class Game(Base):
    __tablename__ = "TicTacToe"

    id = Column(Integer, primary_key=True, index=True)
    player1 = Column(String(100), nullable = False)
    player2 = Column(String(100), nullable = False)    
    movements_played = Column(Integer, nullable = False )
    next_turn = Column(String(50), nullable = False)
    board = Column(String(50), nullable = False)
    winner = Column(String(50), nullable = True)