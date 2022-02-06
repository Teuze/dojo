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
