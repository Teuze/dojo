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
    effects: List[Party]

    def update(self, event: Event):
        if len(self.effects) == 0:
            old_state = self.init
        else:
            old_state = self.effects[-1]

        new_state = event.happen(old_state)

        self.events.append(event)
        self.effects.append(new_state)
