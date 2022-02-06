from pydantic import validator
from pydantic import BaseModel
from core.player import Player
from typing import List


class Party(BaseModel):

    """Dataclass containing playing characters."""

    members: List[Player]
    playing: int = 0

    @validator("playing")
    def playing_validation(cls, v, values):
        e1 = "Playing turn cannot be negative."
        e2 = "Playing turn cannot be higher than player count."

        if v < 0:
            raise ValueError(e1)

        if v >= len(values["members"]):
            raise ValueError(e2)
