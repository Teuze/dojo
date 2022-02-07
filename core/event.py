from dataclasses import dataclass
from typing import List, Type
from enum import Enum

from core.zone import RadialZone
import core.utils as checking
import core.zone as z


@dataclass(frozen=True)
class Action:

    """Abstract dataclass defining playable events."""

    cost: int
    cooldown: int

    def __post_init__(self):

        e = "Action cost cannot be negative."
        if self.cost < 0:
            raise Exception(e)

        e = "Action cooldown cannot be negative."
        if self.cooldown < 0:
            raise Exception(e)

    def check_action(self, player, players, history) -> None:
        checking.check_presence(player, players)
        checking.check_turn(player, players)
        checking.check_playbook(self, player)
        checking.check_cooldown(self, player, history)
        checking.check_cost(self, player)

    def apply(self, player, **game):  # -> Players
        raise NotImplementedError()


@dataclass(frozen=True)
class Intent(Action):

    """Abstract dataclass defining actions on positional targets."""

    visible: bool
    walkable: bool
    available: bool
    range: RadialZone

    def check_target(self, target, player, players, board) -> None:
        checking.check_range(self, player, target)
        checking.check_walkability(self, target, board)
        checking.check_availability(self, target, players)
        checking.check_visibility(self, player, target, players, board)

    def apply(self, target, player, **game):  # -> Players
        raise NotImplementedError()


History = List[Type[Action]]


@dataclass(frozen=True)
class Pass(Action):
    cost: int = 0
    cooldown: int = 0

    def apply(self, player, **game):  # -> Players
        players = game["players"].copy()
        players.next()
        return players


@dataclass(frozen=True)
class Suicide(Action):
    cost: int = 0
    cooldown: int = 0

    def apply(self, player, **game):  # -> Players
        players = game["players"].copy()
        del players.index[player]
        return players


@dataclass(frozen=True)
class Walk(Intent):
    cost: int = 1
    cooldown: int = 0
    visible: bool = True
    walkable: bool = True
    available: bool = True

    range: RadialZone = z.Rhombus(radius=(1, 1))


@dataclass(frozen=True)
class Push(Intent):
    cost: int = 3
    cooldown: int = 1
    visible: bool = True
    walkable: bool = True
    available: bool = False

    range: RadialZone = z.Plus(radius=(1, 4))


@dataclass(frozen=True)
class Pull(Intent):
    cost: int = 3
    cooldown: int = 1
    visible: bool = True
    walkable: bool = True
    available: bool = False

    range: RadialZone = z.Plus(radius=(1, 4))


@dataclass(frozen=True)
class Teleport(Intent):
    cost: int = 4
    cooldown: int = 1
    visible: bool = False
    walkable: bool = True
    available: bool = False

    range: RadialZone = z.Rhombus(radius=(1, 4))


@dataclass(frozen=True)
class Switch(Intent):
    cost: int = 4
    cooldown: int = 0
    visible: bool = False
    walkable: bool = True
    available: bool = False

    range: RadialZone = z.Rhombus(radius=(1, 4))


@dataclass(frozen=True)
class Kill(Intent):
    cost: int = 6
    cooldown: int = 2
    visible: bool = True
    walkable: bool = True
    available: bool = False

    range: RadialZone = z.Rhombus(radius=(1, 1))


class Attack(Intent):
    power: int


class Heal(Intent):
    power: int


class BuffType(Enum):
    ACTION, HEALTH, LEVEL = 1, 2, 3


class Buff(Intent):
    buff_type: BuffType
    power: int
    pass
