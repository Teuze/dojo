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

    @validator("turn")
    def normalize_turn(cls, v, values):
        e = "Playing turn is invalid."
        if v < 0 or v >= len(values["players"]):
            raise ValueError(e)
        return v

    @validator("board")
    def normalize_board(cls, v, values):
        e = "Player is outside board dimensions."
        positions = [player.position for player in values["players"]]
        for p in positions:
            c0 = p[0] > v.shape[0] or p[0] < 0
            c1 = p[1] > v.shape[1] or p[1] < 0
            if c0 or c1:
                raise ValueError(e)
        return v

    @validator("players")
    def normalize_players(cls, v):
        e1 = "Players cannot be on the same Position."
        positions = [player.position for player in v]
        counts = [positions.count(pos) for pos in positions]
        counts = [c for c in counts if c > 1]

        if len(counts) > 0:
            raise ValueError(e1)

        def double_sort(x):
            teams = [p.team for p in v]
            return (x.level, -teams.count(x.team))

        return sorted(v, key=lambda x: double_sort(x), reverse=True)

    @validator("events")
    def normalize_events(cls, v):
        # TODO: Implement dynamic checks on update
        return v