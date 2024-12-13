#!/usr/bin/env python3
from __future__ import annotations

import collections
import dataclasses
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import Pos


@dataclasses.dataclass(frozen=True)
class Map:
    heights: dict[Pos, int]
    size: Pos


def part1(map: Map) -> int:
    nines = [pos for pos, height in map.heights.items() if height == 9]
    to_nine = {pos: {pos} for pos in nines}
    todo = collections.deque(nines)
    seen = set(nines)
    while todo:
        pos = todo.popleft()
        step = map.heights[pos]
        for neighbor in pos.orthogonal_neighbors_sized(map.size):
            if map.heights[neighbor] == step - 1:
                to_nine.setdefault(neighbor, set())
                to_nine[neighbor].update(to_nine[pos])
                if neighbor not in seen:
                    seen.add(neighbor)
                    todo.append(neighbor)

    count = 0
    for pos, height in map.heights.items():
        if height == 0:
            count += len(to_nine[pos])
    return count


def part2(map: Map) -> int:
    nines = [pos for pos, height in map.heights.items() if height == 9]
    trails = {pos: 1 for pos in nines}
    todo = collections.deque(nines)
    seen = set(nines)
    while todo:
        pos = todo.popleft()
        step = map.heights[pos]
        for neighbor in pos.orthogonal_neighbors_sized(map.size):
            if map.heights[neighbor] == step - 1:
                trails.setdefault(neighbor, 0)
                trails[neighbor] += trails[pos]
                if neighbor not in seen:
                    seen.add(neighbor)
                    todo.append(neighbor)

    count = 0
    for pos, height in map.heights.items():
        if height == 0:
            count += trails[pos]
    return count


def parse_map(input: str) -> Map:
    heights = {}
    lines = input.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            heights[Pos(y, x)] = int(c)
    size = Pos(len(lines), len(lines[0]))
    return Map(heights, size)


def main(p: pathlib.Path) -> None:
    map = parse_map(p.read_text())
    print(f"part 1: {part1(map)}")
    print(f"part 2: {part2(map)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
