from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Pos:
    y: int
    x: int

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Pos(self.y - other.y, self.x - other.x)

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

    def in_bounds(self, map_size: Pos) -> bool:
        return 0 <= self.x < map_size.x and 0 <= self.y < map_size.y

    def orthogonal_neighbors_sized(self, map_size: Pos):
        poses = self.orthogonal_neighbors()
        return [p for p in poses if p.in_bounds(map_size)]

    def manhattan_distance(self, other: Pos) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRS_8 = [
    Pos(-1, -1),
    Pos(-1, 0),
    Pos(-1, 1),
    Pos(0, -1),
    Pos(0, 1),
    Pos(1, -1),
    Pos(1, 0),
    Pos(1, 1),
]
