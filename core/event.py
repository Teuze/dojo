from pydantic import BaseModel, validator

from copy import deepcopy

from core import Position
from core.action import Action
from core.player import Player
from core.party import Party
from core.zone import Rhombus


class Event(BaseModel):

    """Dataclass defining actions applied by a player on a target."""

    action: Action
    player: Player
    target: Position

    @validator("player")
    def check_playbook(cls, v, values):
        e = "Action not in player's playbook."
        if "action" in values:
            player = v
            action = values["action"].__class__.__name__
            if action not in player.playbook:
                raise ValueError(e)
        return v

    @validator("player")
    def check_cost(cls, v, values):
        e = "Player hasn't enough actions left."
        if "action" in values:
            player = v
            action = values["action"]
            if action.cost > player.actions[0]:
                raise ValueError(e)
        return v

    @validator("target")
    def check_range(cls, v, values):
        e = "Target is outside of range."
        if "action" in values and "player" in values:
            target = v
            action = values["action"]
            player = values["player"]
            dx = target[0] - player.position[0]
            dy = target[1] - player.position[1]
            if (dx, dy) not in Rhombus(radius=action.range).zone():
                raise ValueError(e)
        return v

    def happen(self, players: Party) -> Party:
        # TODO: unf*ck this mess
        actions = self.player.actions
        new_players = deepcopy(players)
        new_player = deepcopy(self.player)
        result = self.action.apply(self.target, new_player, new_players)
        new_player.actions = (actions[0] - self.action.cost, actions[1])
        return result
