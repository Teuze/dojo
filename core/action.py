from pydantic import validator
from pydantic import BaseModel
from pydantic import PositiveInt
from typing import Optional
from core.zone import Zone
from core import normalize_range
from core import Range


class Action(BaseModel):

    """Dataclass defining playable actions."""

    cost: PositiveInt
    cooldown: PositiveInt
    visible: Optional[bool]
    walkable: Optional[bool]
    available: Optional[bool]
    range: Range
    impact: Zone

    _range = validator("range", allow_reuse=True)(normalize_range)
