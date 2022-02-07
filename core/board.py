from dataclasses import dataclass, field, asdict
from typing_extensions import TypeAlias
from typing import Tuple, List, Dict

Position: TypeAlias = Tuple[int, int]


@dataclass
class Cell:

    """Dataclass defining positional attributes."""

    sprite: str = ""
    fixture: str = ""
    walkable: bool = False
    seethrough: bool = True

    def repr(self, pname: str = "") -> str:

        tiles = "<.> [.] {.} (.)"

        selector = 2 * self.walkable + self.seethrough

        if len(pname) > 0:
            tiles.replace(".", pname[0])
        result = tiles.split()[selector]

        return result

    def draw(self, pname: str = "") -> None:
        print(self.repr(pname))


@dataclass
class Board:

    """2D Array of Cell objects representing terrain features."""

    name: str
    shape: Position
    spawn: List[Position] = field(repr=False, default_factory=list)
    cells: Dict[Position, Cell] = field(repr=False, default_factory=dict)

    def __post_init__(self) -> None:

        e = "Board dimensions should be strictly positive."
        if self.shape[0] <= 0 or self.shape[1] <= 0:
            raise Exception(e)

        e = "Not enough spawn spots to play."
        if len(self.cells) < len(self.spawn):
            raise Exception(e)

        if len(self.spawn) < 2:
            raise Exception(e)

        for pos in self.spawn:

            e = "Spawn outside of board boundaries."
            if pos[0] < 0 or pos[0] >= self.shape[0]:
                raise Exception(e)

            if pos[1] < 0 or pos[1] >= self.shape[1]:
                raise Exception(e)

            e = "Multiple spawns for same position."
            if self.spawn.count(pos) != 1:
                raise Exception(e)

            e = "Spawn spot is not walkable."
            if not self[pos].walkable:
                raise Exception(e)

        for pos in self.cells:

            e = "Position outside of board boundaries."
            if pos[0] < 0 or pos[0] >= self.shape[0]:
                raise Exception(e)

            if pos[1] < 0 or pos[1] >= self.shape[1]:
                raise Exception(e)

    def __getitem__(self, pos: Position) -> Cell:
        
        e = "Position outside of board boundaries."
        if pos[0] < 0 or pos[0] >= self.shape[0]:
                raise Exception(e)

        if pos[1] < 0 or pos[1] >= self.shape[1]:
                raise Exception(e)

        if pos not in self.cells: return Cell()

        else: return self.cells[pos]

    def repr(self, players=None) -> str:
        line: str = ""
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                # TODO: inject optional player names in that
                line = line + self.cells[x, y].repr() + " "
            line = line[:-1] + "\n"
        return line[:-1]

    def draw(self, players=None) -> None:
        print(self.repr(players))
