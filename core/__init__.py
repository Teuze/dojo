from typing import Tuple, List
from typing_extensions import TypeAlias

Position: TypeAlias = Tuple[int, int]

Zone: TypeAlias = List[Position]


def normalize_range(r: Tuple[int, int]) -> Tuple[int, int]:
    e1 = "Radius cannot be negative."
    e2 = "Radius should be low-to-high."

    if r[0] < 0 or r[1] < 0:
        raise ValueError(e1)

    if r[1] < r[0]:
        raise ValueError(e2)

    return r
