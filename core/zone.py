from math import atan2
from typing import Tuple, Set, List
from typing_extensions import TypeAlias
from dataclasses import dataclass

Position: TypeAlias = Tuple[int, int]

Zone: TypeAlias = Set[Position]


@dataclass
class RadialZone:

    """Abstract dataclass defining positional ranges."""

    center: Position = (0, 0)
    radius: Position = (0, 0)

    def __post_init__(self) -> None:

        e = "Radius cannot be negative."
        if self.radius[0] <= self.radius[1] < 0:
            raise Exception(e)

        e = "Radius should be low-to-high."
        if self.radius[1] < self.radius[0]:
            raise Exception(e)

        self.zone: Zone = self._zone(self.center, self.radius)

    def _zone(self, center: Position, radius: Position) -> Zone:
        raise NotImplementedError()

    def sort(self) -> List[Position]:
        """Sort positions by their distance to center (clockwise)."""

        def radius(p: Position):
            distance = abs(p[0] - self.center[0])
            distance += abs(p[1] - self.center[1])
            return distance

        def double_sort(p):
            return (radius(p), -atan2(p[0], p[1]))

        return sorted(self.zone, key=double_sort)


class Rhombus(RadialZone):
    def _zone(self, center: Position, radius: Position) -> Zone:
        ra, rb = radius
        cx, cy = center
        zone = []
        if radius == (0, 0):
            zone.append(center)
        for i in range(ra, rb + 1):
            l1 = line((cx + i, cy), (cx, cy - i))
            l2 = line((cx, cy - i), (cx - i, cy))
            l3 = line((cx - i, cy), (cx, cy + i))
            l4 = line((cx, cy + i), (cx + i, cy))
            zone += l1 + l2 + l3 + l4
        return set(zone)


class Square(RadialZone):
    def _zone(self, center: Position, radius: Position) -> Zone:
        ra, rb = radius
        cx, cy = center
        zone = []
        if self.radius == (0, 0):
            zone.append(center)
        for i in range(ra, rb + 1):
            l1 = line((cx + i, cy + i), (cx + i, cy - i))
            l2 = line((cx + i, cy - i), (cx - i, cy - i))
            l3 = line((cx - i, cy - i), (cx - i, cy + i))
            l4 = line((cx - i, cy + i), (cx + i, cy + i))
            zone += l1 + l2 + l3 + l4
        return set(zone)


class Plus(RadialZone):
    def _zone(self, center: Position, radius: Position) -> Zone:
        ra, rb = radius
        cx, cy = center
        zone = []
        if self.radius == (0, 0):
            zone.append(center)
        l1 = line((cx + ra, cy), (cx + rb, cy))
        l2 = line((cx - ra, cy), (cx - rb, cy))
        l3 = line((cx, cy + ra), (cx, cy + rb))
        l4 = line((cx, cy - ra), (cx, cy - rb))
        zone += l1 + l2 + l3 + l4
        return set(zone)


class Cross(RadialZone):
    def _zone(self, center: Position, radius: Position) -> Zone:
        ra, rb = radius
        cx, cy = center
        zone = []
        if self.radius == (0, 0):
            zone.append(center)
        l1 = line((cx + ra, cy + ra), (cx + rb, cy + rb))
        l2 = line((cx + ra, cy - ra), (cx + rb, cy - rb))
        l3 = line((cx - ra, cy - ra), (cx - rb, cy - rb))
        l4 = line((cx - ra, cy + ra), (cx - rb, cy + rb))
        zone += l1 + l2 + l3 + l4
        return set(zone)


def line(pos1: Position, pos2: Position) -> List[Position]:

    """Bresenham's Line Algorithm
    Produces a list of tuples from pos1 to pos2
    [Source code from RogueBasin.com]"""

    # Setup initial conditions
    x1, y1 = pos1
    x2, y2 = pos2

    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary, store swap state
    swapped = False

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate point generation from start to end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()

    return points
