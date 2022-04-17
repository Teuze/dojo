from pydantic import BaseModel, NonNegativeInt, validator

from typing import List
from copy import deepcopy

from core.player import Player
from core.board import Board
from core.event import Event
from core.zone import line


class Game(BaseModel):

    """Dataclass containing the game history and current state."""

    players: List[Player]
    events: List[Event]
    board: Board

    turn: NonNegativeInt = 0

    def update(self, event: Event) -> None:
        e1 = "It is not player's turn."
        if event.player != self.players[self.turn]:
            raise ValueError(e1)

        e2 = "Action has not cooled down yet."
        cooldown : int = event.action.cooldown
        last_use : int = 0
        for e in self.events[::-1]:
            c1 = e.player.name == event.player.name
            c2 = e.action.name == event.action.name
            c3 = e.action.name == "Pass"
            if c1 and c3:
                last_use += 1
            if c1 and c2:
                break
        if cooldown > last_use:
            raise ValueError(e2)

        e3 = "Target is out of sight."
        positions = line(event.player.position, event.target)
        for pos in positions[1:-1]:
            cell = Board.cells[Board.cells.index(pos)]
            c1 = not cell.seethrough
            c2 = pos in [p.position for p in self.players]
            if c1 or c2:
                raise ValueError(e3)

        # TODO: Implement availability

        t = self.turn
        r = event.happen(deepcopy(self.players))

        if event.action.__class__.__name__ == "Pass": t += 1

        # Remove all players with zero health or less
        # Adjust playing turn accordingly

        for player in r:
            if player.health[0] <= 0:
                t = (t-1) if player.index < t else t
                del player

        # Update game in-place
        self.turn = t % len(r)
        self.events += [event]
        self.players = r

        return

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

    @validator("board")
    def normalize_board(cls, v, values):
        if "player" not in values:
            return v

        e = "Player is outside board dimensions."
        positions = [player.position for player in values["players"]]
        for p in positions:
            c0 = p[0] > v.shape[0] or p[0] < 0
            c1 = p[1] > v.shape[1] or p[1] < 0
            if c0 or c1:
                raise ValueError(e)
        return v

    @validator("turn")
    def normalize_turn(cls, v, values):
        if "player" not in values:
            return v

        e = "Playing turn is invalid."
        if v < 0 or v >= len(values["players"]):
            raise ValueError(e)
        return v

    @validator("events")
    def normalize_events(cls, v):
        return v
