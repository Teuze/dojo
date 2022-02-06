from pydantic import BaseModel

from core import Position
from core.action import Action
from core.player import Player


class Event(BaseModel):

    """Dataclass defining actions applied by a player on a target."""

    action: Action
    player: Player
    target: Position
