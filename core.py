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



def place_entity(state: GameState, entity, x: int, y: int):
    state.grid[y][x] = entity


def find_character(state: GameState) -> Character:
    for y in range(state.height):
        for x in range(state.width):
            if isinstance(state.grid[y][x], Character):     # returns True if cell is a Character, False otherwise
                return (x,y)   #returning the coordinates of the character
    return None


def move_character(state: GameState, direction: str):
    char_pos = find_character(state)
    if char_pos is None:
        return  # No character found

    x, y = char_pos
    new_x, new_y = x, y

    if direction == "W":
        new_y -= 1
        state.grid[y][x].direction = "up"   #character now facing up 
    elif direction == "S":
        new_y += 1
        state.grid[y][x].direction = "down" #character now facing down
    elif direction == "A":
        new_x -= 1
        state.grid[y][x].direction = "left"    #character now facing left
    elif direction == "D":
        new_x += 1
        state.grid[y][x].direction = "right"   #character now facing right

    # Check boundaries
    if 0 <= new_x < state.width and 0 <= new_y < state.height and not isinstance(state.grid[new_y][new_x],Tree):
        # Move character to the new position
        state.grid[new_y][new_x] = state.grid[y][x]
        state.grid[y][x] = None  # Clear the old position