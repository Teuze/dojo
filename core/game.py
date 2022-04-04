from pydantic import BaseModel

from typing import List

from core.party import Party
from core.board import Board
from core.event import Event


class Game(BaseModel):

    """Dataclass containing the game history, board and initial state."""

    init: Party
    board: Board
    events: List[Event]
    states: List[Party]

    def update(self, event: Event):
        if len(self.states) == 0:
            old_state = self.init
        else:
            old_state = self.states[-1]

        new_state = event.happen(old_state)

        self.events.append(event)
        self.states.append(new_state)
