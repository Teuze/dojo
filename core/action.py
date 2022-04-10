from pydantic import validator
from pydantic import BaseModel
from pydantic import NonNegativeInt

from typing import Optional

from core.zone import Zone
from core.zone import Rhombus

from core import normalize_range
from core import Range


class Action(BaseModel):

    """Dataclass defining playable actions."""

    cost: NonNegativeInt
    cooldown: NonNegativeInt
    visible: Optional[bool]
    walkable: Optional[bool]
    available: Optional[bool]
    range: Range
    impact: Zone

    _range = validator("range", allow_reuse=True)(normalize_range)

    def apply(self, position, player, players):
        raise NotImplementedError()

class Pass(Action):

    cost: NonNegativeInt = 0
    cooldown: NonNegativeInt = 0
    visible: Optional[bool] = None
    walkable: Optional[bool] = None
    available: Optional[bool] = None
    range: Range = (0,0)
    impact: Zone = Rhombus()

    def apply(self, position, player, players):
        return players

class Move(Action):

    cost: NonNegativeInt = 1
    cooldown: NonNegativeInt = 0
    visible: Optional[bool] = None
    walkable: Optional[bool] = True
    available: Optional[bool] = True
    range: Range = (1, 1)
    impact: Zone = Rhombus()

    def apply(self, position, player, players):
        index = players.index(player)
        player.position = position
        players[index] = player
        return players
