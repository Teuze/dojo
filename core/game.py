from pydantic import BaseModel, NonNegativeInt, validator

from typing import List

from core.player import Player
from core.board import Board
from core.event import Event


class Game(BaseModel):

    """Dataclass containing the game history and current state."""

    turn: NonNegativeInt = 0
    board: Board
    events: List[Event]
    players: List[Player]

    def update(self, event: Event):
        t = self.turn
        b = self.board
        e = self.events + [event]
        p = event.happen(t, b, e, p)
        # if event.action.__name__ == "Pass": t += 1
        return Game(turn=t, board=b, events=e, players=p)

    @property
    def finished(self) -> bool:
        pass

    @property
    def winners(self) -> List[Player]:
        pass

    @property
    def losers(self) -> List[Player]:
        pass

    @validator("turn")
    def normalize_turn(cls, v, values):
        e1 = "Playing turn cannot be negative."
        e2 = "Playing turn cannot be higher than player count."

        if v < 0:
            raise ValueError(e1)

        if v >= len(values["players"]):
            raise ValueError(e2)

        return v

    @validator("players")
    def normalize_players(cls, v):
        e1 = "Players cannot be on the same Position."
        e2 = "Players cannot be outside board dimensions."

        positions = [player.position for player in v]
        counts = [positions.count(pos) for pos in positions]
        counts_sup1 = [c for c in counts if c > 1]

        if len(counts_sup1) > 0:
            raise ValueError(e1)

        # TODO: Implement board dimensions check

        def double_sort(x):
            teams = [p.team for p in v]
            return (x.level, -teams.count(x.team))

        return sorted(v, key=lambda x: double_sort(x), reverse=True)

    @validator("events")
    def normalize_events(cls, v):
        # TODO: Implement board dimensions check
        # TODO: Implement cooldown check
        # TODO: Implement action player turn verification
        return v