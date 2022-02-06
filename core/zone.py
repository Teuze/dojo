from pydantic import BaseModel
from pydantic import validator

from core import Position
from core import normalize_range


class RadialZone(BaseModel):

    """Dataclass defining positional ranges."""

    center: Position = (0, 0)
    radius: Position = (0, 0)

    _radius = validator("radius", allow_reuse=True)(normalize_range)
