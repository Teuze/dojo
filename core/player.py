from dataclasses import dataclass, field
from typing import Tuple, List


def _playbook():
    return ["Pass", "Move", "Suicide"]


_playfield = field(repr=False, default_factory=_playbook)


@dataclass
class Player:

    """Dataclass defining character statistics."""

    name: str
    team: str
    level: int
    health: Tuple[int, int]
    actions: Tuple[int, int]
    position: Tuple[int, int]
    playbook: List = _playfield

    def __post_init__(self):

        e = "Action points should be high-to-low."
        if self.actions[1] > self.actions[0]:
            return Exception(e)

        e = "Health points should be high-to-low."
        if self.health[1] > self.health[0]:
            return Exception(e)

        e = "Health should be strictly positive."
        if self.health[0] <= self.health[1] <= 0:
            return Exception(e)

        e = "Level should be strictly positive."
        if self.level <= 0:
            return Exception(e)


@dataclass
class Players:

    """Supercharged collection of Player objects."""

    members: List[Player]
    playing: int = 0

    def __post_init__(self) -> None:

        e = "Playing turn cannot be negative."
        if self.playing < 0:
            raise Exception(e)

        e = "Playing turn cannot be higher than player count."
        if self.playing >= len(self.members):
            raise Exception(e)

        e = "Players cannot be on the same Position."
        counts = [self.members.count(p.position) for p in self.members]
        counts_sup1 = [c for c in counts if c>1]
        if len(counts_sup1) > 0:
            raise Exception(e)

        e = "Players cannot have the same name."
        counts = [self.members.count(p.name) for p in self.members]
        counts_sup1 = [c for c in counts if c>1]
        if len(counts_sup1) > 0:
            raise Exception(e)

        def double_sort(x):
            return (x.level, self.members.count(x.team))

        self.members = sorted(self.members, key=double_sort, reverse=True)

    def spawn(self, new_player: Player) -> None:

        new_party = Players(self.members + [new_player])
        index = new_party.members.index(new_player)
        if index < self.playing:
            self.playing += 1

        self.members = new_party.members

    def kill(self, player_index: int) -> None:

        if player_index < self.playing and self.playing > 0:
            self.playing -= 1

        del self.members[player_index]

    def next(self) -> None:
        self.playing = (self.playing + 1) % len(self.members)
