from pydantic import BaseModel, PositiveInt, validator, constr
from typing import List
from core import Position, Range
from core import normalize_range


class Player(BaseModel):

    """Dataclass defining character statistics."""

    name: constr(min_length=4, max_length=24, strip_whitespace=True)
    team: constr(min_length=4, max_length=24, strip_whitespace=True)
    level: PositiveInt
    position: Position
    health: Range
    actions: Range
    playbook: List[str]

    _action = validator("actions", allow_reuse=True)(normalize_range)
    _health = validator("health", allow_reuse=True)(normalize_range)
