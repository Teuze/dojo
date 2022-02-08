from pydantic import validator
from pydantic import BaseModel
from core.player import Player
from typing import List


class Party(BaseModel):

    """Dataclass containing playing characters."""

    members: List[Player]
    playing: int = 0

    @validator("playing")
    def normalize_playing(cls, v, values):
        e1 = "Playing turn cannot be negative."
        e2 = "Playing turn cannot be higher than player count."

        if v < 0:
            raise ValueError(e1)

        if v >= len(values["members"]):
            raise ValueError(e2)

        return v

    @validator("members")
    def normalize_members(cls, v):
        e = "Players cannot be on the same Position."
        positions = [player.position for player in v]
        counts = [positions.count(pos) for pos in positions]
        counts_sup1 = [c for c in counts if c > 1]

        if len(counts_sup1) > 0:
            raise Exception(e)

        def double_sort(x):
            teams = [p.team for p in v]
            return (x.level, -teams.count(x.team))

        return sorted(v, key=lambda x: double_sort(x), reverse=True)
