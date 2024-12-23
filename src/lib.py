from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Pos:
    y: int
    x: int

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)

    def top(self) -> Pos:
        return Pos(self.y - 1, self.x)

    def bottom(self) -> Pos:
        return Pos(self.y + 1, self.x)

    def left(self) -> Pos:
        return Pos(self.y, self.x - 1)

    def right(self) -> Pos:
        return Pos(self.y, self.x + 1)

    def orthogonal_neighbors(self):
        return [
            Pos(self.y, self.x + 1),
            Pos(self.y, self.x - 1),
            Pos(self.y + 1, self.x),
            Pos(self.y - 1, self.x),
        ]

    def orthogonal_neighbors_sized(self, map_size: Pos):
        poses = [
            Pos(self.y, self.x + 1),
            Pos(self.y, self.x - 1),
            Pos(self.y + 1, self.x),
            Pos(self.y - 1, self.x),
        ]
        return [p for p in poses if 0 <= p.x < map_size.x and 0 <= p.y < map_size.y]

    def manhattan_distance(self, other: Pos) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
