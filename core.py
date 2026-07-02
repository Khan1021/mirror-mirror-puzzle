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
    
    land_x,land_y=x,y

    while True:
        if direction =="up":
            y-=1
        elif direction =="down":
            y+=1
        elif direction =="left":
            x-=1
        elif direction =="right":
            x+=1
    
        # Check boundaries of grid
        if not (0<=x<state.width and  0<=y<state.height):
            break   #hit the wall

        #check if projectile hits tree, stop projectile 
        if isinstance(state.grid[y][x],Tree):
            break   #hit a Tree

        land_x, land_y = x, y

        #check if projectile hits a mirror, bounce and keep playing
        if isinstance(state.grid[y][x],Mirror):
           direction=reflect(direction,state.grid[y][x].angle)   #hit a mirror, reflect the projectile

        #check if projectile hits a crate, returns True so user can finish game
        if isinstance(state.grid[y][x],Crate):
            state.grid[char_pos[1]][char_pos[0]]=None   #clear old position of character
            state.grid[y][x]=character      #character teleports onto crate cell
            character.direction=direction   #face new direction
            return True   #crate destroyed, game won

    #projectile stopped without hitting a crate - teleport character to last safe cell
    state.grid[char_pos[1]][char_pos[0]] = None
    state.grid[land_y][land_x] = character
    character.direction = direction


#main loop needed to run function
def run_game(state: GameState,instructions:str):
    state=copy.deepcopy(state)    #create a copy of the state so that the state does not point to the same object and change together
    steps=[]
    
    for instruction in instructions:
        if instruction in ["W","A","S","D"]:
            if move_character(state, instruction):
                steps.append(copy.deepcopy(state))
                return True, steps   #crate destroyed, game won
            steps.append(copy.deepcopy(state))

        elif instruction == "X":
            if shoot(state):
                steps.append(copy.deepcopy(state))
                return True, steps   #crate destroyed, game won
            steps.append(copy.deepcopy(state))

    #if loop reaches here, game is not won
    return steps