from dataclasses import dataclass

@dataclass
class Character:
    direction: str   #"up", "down", "left", "right"


@dataclass
class Tree:
    pass    #pass == no properties needed


@dataclass
class Mirror:
    angle: int


@dataclass
class Crate:
    pass



@dataclass
class GameState:
    width: int
    height: int
    grid: list



def create_game_state(width: int, height: int) -> GameState:
    #creating a grid filled with None 
    grid =[[None for _ in range(width)] for _ in range(height)]

    return GameState(width, height, grid)