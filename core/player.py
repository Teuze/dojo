from pydantic import BaseModel, PositiveInt, validator
from typing import List
from core import Position, Range
from core import normalize_range


class Player(BaseModel):

    """Dataclass defining character statistics."""

    name: str
    team: str
    level: PositiveInt
    position: Position
    health: Range
    actions: Range
    playbook: List[str]

    _action = validator("actions", allow_reuse=True)(normalize_range)
    _health = validator("health", allow_reuse=True)(normalize_range)
