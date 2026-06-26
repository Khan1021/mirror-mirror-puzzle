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