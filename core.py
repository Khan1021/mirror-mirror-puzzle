from dataclasses import dataclass
import copy


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
        if isinstance(state.grid[new_y][new_x],Crate):
            character = state.grid[y][x]
            state.grid[y][x] = None   #clear old position
            state.grid[new_y][new_x] = character   #character moves onto crate cell, destroying it
            return True   #crate destroyed and game won
        # Move character to the new position
        state.grid[new_y][new_x] = state.grid[y][x]
        state.grid[y][x] = None  # Clear the old position

    


#takes current direction of projectile and mirror's angle, return new direction of projectile after reflection
def reflect(direction: str,angle: int) -> str:
    if angle == 45:
        if direction == "right":
            return "up"
        if direction == "left":
            return "down"
        if direction == "up":
            return "right"
        if direction == "down":
            return "left"
    if angle == -45:
        if direction == "right":
            return "down"
        if direction == "left":
            return "up"
        if direction == "up":
            return "left"
        if direction == "down":
            return "right"


def shoot(state: GameState):
    char_pos=find_character(state)
    if char_pos==None:
        return None #no character found

    x,y=char_pos
    character = state.grid[y][x]
    direction = character.direction

    #Phase 1: travel from the character until a mirror is hit, counting the distance
    cx,cy=x,y
    distance=0
    while True:
        if direction=="up":
            cy-=1
        elif direction=="down":
            cy+=1
        elif direction=="left":
            cx-=1
        elif direction=="right":
            cx+=1
        distance+=1

        if not (0<=cx<state.width and 0<=cy<state.height):
            return None   #hit a wall before any mirror, X does nothing

        if isinstance(state.grid[cy][cx],Tree):
            return None   #hit a tree before any mirror, X does nothing

        if isinstance(state.grid[cy][cx],Crate):
            state.grid[y][x]=None
            state.grid[cy][cx]=character
            character.direction=direction
            return True   #hit crate directly, game won

        if isinstance(state.grid[cy][cx],Mirror):
            direction=reflect(direction,state.grid[cy][cx].angle)   #reflect, move to phase 2
            break

    #Phase 2: travel exactly `distance` cells in the reflected direction
    steps_taken=0
    while steps_taken<distance:
        if direction=="up":
            cy-=1
        elif direction=="down":
            cy+=1
        elif direction=="left":
            cx-=1
        elif direction=="right":
            cx+=1
        steps_taken+=1

        if not (0<=cx<state.width and 0<=cy<state.height):
            return None   #blocked before completing the distance, X does nothing

        if isinstance(state.grid[cy][cx],Tree):
            return None   #blocked before completing the distance, X does nothing

        if isinstance(state.grid[cy][cx],Crate):
            state.grid[y][x]=None
            state.grid[cy][cx]=character
            character.direction=direction
            return True   #landed on crate, game won

        if isinstance(state.grid[cy][cx],Mirror):
            direction=reflect(direction,state.grid[cy][cx].angle)   #bounce again, keep going

    #completed the full distance without hitting anything blocking
    state.grid[y][x]=None
    state.grid[cy][cx]=character
    character.direction=direction
    return None   #moved, but not a win


#main loop needed to run function
def run_game(state: GameState,instructions:str):
    state=copy.deepcopy(state)    #create a copy of the state so that the state does not point to the same object and change together
    steps=[]
    
    for instruction in instructions:
        if instruction in ["W","A","S","D"]:
            won = move_character(state, instruction)
            steps.append(copy.deepcopy(state))
            if won:
                return True, steps   #crate destroyed, game won

        elif instruction == "X":
            won = shoot(state)
            steps.append(copy.deepcopy(state))
            if won:
                return True, steps   #crate destroyed, game won

    #instructions finished without winning
    return False, steps


#converts a single grid cell (entity or None) into a JSON-friendly dict tagged with its type
def entity_to_dict(entity):
    if entity is None:
        return None
    if isinstance(entity, Character):
        return {"type": "character", "direction": entity.direction}
    if isinstance(entity, Tree):
        return {"type": "tree"}
    if isinstance(entity, Mirror):
        return {"type": "mirror", "angle": entity.angle}
    if isinstance(entity, Crate):
        return {"type": "crate"}


def state_to_dict(state: GameState):
    return {
        "width": state.width,
        "height": state.height,
        "grid": [[entity_to_dict(cell) for cell in row] for row in state.grid],
    }


#runs the game and returns a JSON-friendly dict with the final result and every intermediate step
def export_game(state: GameState, instructions: str):
    won, steps = run_game(state, instructions)
    return {
        "won": won,
        "steps": [state_to_dict(step) for step in steps],
    }