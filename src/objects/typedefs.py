
from __future__ import annotations
from enum import Enum
    
class Move(Enum):
    PLAY_TILE = "add tile"
    DRAW_TILE = "draw"
    PASS_MOVE = "Pass this turn."

class Orientation(Enum):
    LEFT = "Left"
    RIGHT = "Right"