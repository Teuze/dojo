from pydantic import BaseModel  # validator
from typing import Tuple, List

# from core import normalize_range
from core import Position
from core.cell import Cell


class Board(BaseModel):

    """2D Array of Cell objects representing terrain features."""

    name: str
    shape: Tuple[int, int]
    spawn: List[Position]
    cells: List[Cell]

    # TODO: Use custom validator for board shape
    # _shape = validator("shape", allow_reuse=True)(normalize_range)
