from pydantic import BaseModel, PositiveInt, validator
from typing import Tuple, List
from core import Position
from core import normalize_range


class Player(BaseModel):

    """Dataclass defining character statistics."""

    name: str
    team: str
    level: PositiveInt
    position: Position
    health: Tuple[int, int]
    actions: Tuple[int, int]
    playbook: List[str]

    _action = validator("action", allow_reuse=True)(normalize_range)
    _health = validator("health", allow_reuse=True)(normalize_range)
