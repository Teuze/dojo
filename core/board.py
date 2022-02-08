from pydantic import BaseModel, validator
from typing_extensions import TypeAlias
from typing import Tuple, List

from core import Position
from core.cell import Cell

Shape: TypeAlias = Tuple[int, int]


class Board(BaseModel):

    """2D Array of Cell objects representing terrain features."""

    name: str
    shape: Shape
    cells: List[Cell]
    spawn: List[Position]

    @validator('shape')
    def normalize_shape(cls, v):
        e = "Board dimensions should be strictly positive."

        if v[0] <= 0 or v[1] <= 0:
            raise ValueError(e)

        return v

    @validator('cells')
    def normalize_cells(cls, v, values):
        e1 = "Not enough cells for board shape."
        e2 = "Too many cells for board shape."
        e3 = "Cell outside of board boundaries."
        e4 = "Multiple cells for same position."

        if "shape" in values:

            cell_number = values["shape"][0] * values["shape"][1]

            if len(v) < cell_number:
                raise ValueError(e1)

            if len(v) > cell_number:
                raise ValueError(e2)

        for cell in v:

            if cell.position[0] < 0 or cell.position[1] < 0:
                raise ValueError(e3)

            if "shape" in values and cell.position[0] >= values['shape'][0]:
                raise ValueError(e3)

            if "shape" in values and cell.position[1] >= values['shape'][1]:
                raise ValueError(e3)

        cell_position_counts = [v.count(cell.position) for cell in v]
        cell_duplicates = [c for c in cell_position_counts if c > 1]

        if len(cell_duplicates) != 0:
            raise ValueError(e4)

        return sorted(v, key=lambda x: x.position)

    @validator('spawn')
    def normalize_spawn(cls, v, values):
        e1 = "Not enough spawn spots to play."
        e2 = "Too many spawn spots for board object."
        e3 = "Spawn outside of board boundaries."
        e4 = "Multiple spawns for same position."
        e5 = "Spawn spot is not walkable."

        if "cells" in values and len(v) > len(values["cells"]):
            raise ValueError(e2)

        if len(v) < 2:
            raise ValueError(e1)

        for index, pos in enumerate(v):

            if pos[0] < 0 or pos[1] < 0:
                raise ValueError(e3)

            if "shape" in values and pos[0] >= values["shape"][0]:
                raise ValueError(e3)

            if "shape" in values and pos[1] >= values["shape"][1]:
                raise ValueError(e3)

            if v.count(pos) != 1:
                raise Exception(e4)

            if "cell" in values and not values["cells"][index].walkable:
                raise ValueError(e5)

        return v