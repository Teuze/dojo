from pydantic import BaseModel
from core import Position


class Cell(BaseModel):

    """Dataclass defining positional attributes."""

    position: Position
    sprite: str = ""
    fixture: str = ""
    walkable: bool = True
    seethrough: bool = True
