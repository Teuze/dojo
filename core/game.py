from pydantic import BaseModel

from typing import List

from core.party import Party
from core.board import Board
from core.event import Event


class Game(BaseModel):

    """Dataclass containing the game history and current state."""

    party: Party
    board: Board
    events: List[Event]
    states: List[Party]

    # TODO: implement recursive checks
    # TODO: Implement winning condition(s)

    def update(self, event: Event):
        board = self.board
        events = self.events + [event]
        states = self.states + [self.party]
        party = event.happen(self.party)
        return Game(party, board, events, states)
