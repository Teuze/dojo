from pydantic import validator
from pydantic import BaseModel
from pydantic import PositiveInt
from typing import Optional
from typing import Tuple
from core.zone import RadialZone
from core import normalize_range


class Action(BaseModel):

    """Dataclass defining playable actions."""

    cost: PositiveInt
    cooldown: PositiveInt
    visible: Optional[bool]
    walkable: Optional[bool]
    available: Optional[bool]
    range: Tuple[int, int]
    impact: RadialZone

    _range = validator("range", allow_reuse=True)(normalize_range)
