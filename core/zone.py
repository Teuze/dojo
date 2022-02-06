from pydantic import BaseModel
from pydantic import validator

from core import Position, Range
from core import normalize_range


class Zone(BaseModel):

    """Dataclass defining positional ranges."""

    center: Position = (0, 0)
    radius: Range = (0, 0)

    _radius = validator("radius", allow_reuse=True)(normalize_range)
