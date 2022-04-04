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

    def update(self, event: Event): pass
