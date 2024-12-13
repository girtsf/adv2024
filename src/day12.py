#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import Pos


@dataclasses.dataclass
class Region:
    plant: str
    cells: set[Pos] = dataclasses.field(default_factory=set)

    def area(self) -> int:
        return len(self.cells)

    def perimeter(self) -> int:
        count = 0
        for pos in self.cells:
            for neighbor in pos.orthogonal_neighbors():
                if neighbor not in self.cells:
                    count += 1
        return count

    def sides(self) -> int:
        min_y = min(p.y for p in self.cells)
        max_y = max(p.y for p in self.cells)
        min_x = min(p.x for p in self.cells)
        max_x = max(p.x for p in self.cells)

        count = 0
        for y in range(min_y, max_y + 1):
            prev_top_fence = False
            prev_bottom_fence = False
            for x in range(min_x, max_x + 1):
                pos = Pos(y, x)
                if pos not in self.cells:
                    prev_top_fence = False
                    prev_bottom_fence = False
                    continue
                top_fence = pos.top() not in self.cells
                bottom_fence = pos.bottom() not in self.cells

                if top_fence and not prev_top_fence:
                    count += 1
                if bottom_fence and not prev_bottom_fence:
                    count += 1

                prev_top_fence = top_fence
                prev_bottom_fence = bottom_fence

        for x in range(min_x, max_x + 1):
            prev_left_fence = False
            prev_right_fence = False
            for y in range(min_y, max_y + 1):
                pos = Pos(y, x)
                if pos not in self.cells:
                    prev_left_fence = False
                    prev_right_fence = False
                    continue
                left_fence = pos.left() not in self.cells
                right_fence = pos.right() not in self.cells

                if left_fence and not prev_left_fence:
                    count += 1
                if right_fence and not prev_right_fence:
                    count += 1

                prev_left_fence = left_fence
                prev_right_fence = right_fence

        return count


def flood_search(map: list[str], pos: Pos, seen: set[Pos]) -> Region:
    region = Region(map[pos.y][pos.x])
    to_search = [pos]
    while to_search:
        pos = to_search.pop()
        if pos in seen:
            continue
        seen.add(pos)
        region.cells.add(pos)
        for new_pos in pos.orthogonal_neighbors():
            if new_pos.y < 0 or new_pos.y >= len(map):
                continue
            if new_pos.x < 0 or new_pos.x >= len(map[0]):
                continue
            if map[new_pos.y][new_pos.x] != region.plant:
                continue
            to_search.append(new_pos)
    return region


def find_regions(map: list[str]) -> list[Region]:
    out = []
    seen = set()

    for y in range(len(map)):
        for x in range(len(map[y])):
            pos = Pos(y, x)
            if pos in seen:
                continue
            region = flood_search(map, pos, seen)
            out.append(region)

    return out


def part1(regions: list[Region]) -> int:
    return sum(r.area() * r.perimeter() for r in regions)


def part2(regions: list[Region]) -> int:
    return sum(r.area() * r.sides() for r in regions)


def main(p: pathlib.Path) -> None:
    input = p.read_text().splitlines()
    regions = find_regions(input)
    print(part1(regions))
    print(part2(regions))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
