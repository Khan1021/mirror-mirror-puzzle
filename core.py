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

    while True:
        if direction =="up":
            y-=1
        elif direction =="down":
            y+=1
        elif direction =="left":
            x-=1
        elif direction =="right":
            x+=1
    
        # Check boundaries
        if not (0<=x<state.width and  0<=y<state.height):
            break   #hit the wall
        if isinstance(state.grid[y][x],Tree):
            break   #hit a Tree

        #check if projectile hits a mirror
        if isinstance(state.grid[y][x],Mirror):
            reflect(direction,state.grid[y][x].angle)   #hit a mirror, reflect the projectile

        #check if projectile hits a crate
        if isinstance(state.grid[y][x],Crate):
            state.grid[y][x]=None   #hit a crate, destroy it
            break
            