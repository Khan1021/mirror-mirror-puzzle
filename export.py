import json
from core import (
    create_game_state,
    place_entity,
    Character,
    Tree,
    Mirror,
    Crate,
    export_game,
)

# Build a 5x5 world:
# character starts at (0,2) facing right, needs to walk down into the
# mirror's row, then shoot right to bounce up and teleport onto the crate.
state = create_game_state(5, 5)
place_entity(state, Character(direction="right"), x=0, y=2)
place_entity(state, Mirror(angle=45), x=3, y=4)
place_entity(state, Crate(), x=3, y=0)
place_entity(state, Tree(), x=0, y=0)
place_entity(state, Tree(), x=4, y=0)
place_entity(state, Tree(), x=4, y=4)

instructions = "SSDXWW"

result = export_game(state, instructions)

with open("game_data.json", "w") as f:
    json.dump(result, f, indent=2)

print("won:", result["won"])
print("steps:", len(result["steps"]))
