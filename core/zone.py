from pydantic import BaseModel
from pydantic import validator

from typing import List
from math import atan2

from core import Position, Range
from core import normalize_range


class Zone(BaseModel):

    """Dataclass defining positional ranges."""

    center: Position = (0, 0)
    radius: Range = (0, 0)

    _radius = validator("radius", allow_reuse=True)(normalize_range)

    def zone(self) -> List[Position]:
        raise NotImplementedError()

    def sort(self, positions: List[Position]) -> List[Position]:
        """Sort positions by their distance to center (clockwise)."""

        def radius(p):
            distance = abs(p[0] - self.center[0])
            distance += abs(p[1] - self.center[1])
            return distance

        def double_sort(p):
            return (radius(p), -atan2(p[0], p[1]))

        return sorted(positions, key=double_sort)


class Rhombus(Zone):
    def zone(self) -> List[Position]:
        ra, rb = self.radius
        cx, cy = self.center
        zone = []

        if self.radius == (0, 0):
            zone.append(self.center)

        for i in range(ra, rb + 1):
            l1 = line((cx + i, cy), (cx, cy - i))
            l2 = line((cx, cy - i), (cx - i, cy))
            l3 = line((cx - i, cy), (cx, cy + i))
            l4 = line((cx, cy + i), (cx + i, cy))
            zone += l1 + l2 + l3 + l4

        return self.sort(list(set(zone)))


class Square(Zone):
    def zone(self) -> List[Position]:
        ra, rb = self.radius
        cx, cy = self.center
        zone = []

        if self.radius == (0, 0):
            zone.append(self.center)

        for i in range(ra, rb + 1):
            l1 = line((cx + i, cy + i), (cx + i, cy - i))
            l2 = line((cx + i, cy - i), (cx - i, cy - i))
            l3 = line((cx - i, cy - i), (cx - i, cy + i))
            l4 = line((cx - i, cy + i), (cx + i, cy + i))
            zone += l1 + l2 + l3 + l4

        return self.sort(list(set(zone)))


class Plus(Zone):
    def zone(self) -> List[Position]:
        ra, rb = self.radius
        cx, cy = self.center
        zone = []

        if self.radius == (0, 0):
            zone.append(self.center)

        l1 = line((cx + ra, cy), (cx + rb, cy))
        l2 = line((cx - ra, cy), (cx - rb, cy))
        l3 = line((cx, cy + ra), (cx, cy + rb))
        l4 = line((cx, cy - ra), (cx, cy - rb))
        zone += l1 + l2 + l3 + l4

        return self.sort(list(set(zone)))


class Cross(Zone):
    def zone(self) -> List[Position]:
        ra, rb = self.radius
        cx, cy = self.center
        zone = []

        if self.radius == (0, 0):
            zone.append(self.center)

        l1 = line((cx + ra, cy + ra), (cx + rb, cy + rb))
        l2 = line((cx + ra, cy - ra), (cx + rb, cy - rb))
        l3 = line((cx - ra, cy - ra), (cx - rb, cy - rb))
        l4 = line((cx - ra, cy + ra), (cx - rb, cy + rb))
        zone += l1 + l2 + l3 + l4

        return self.sort(list(set(zone)))


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
