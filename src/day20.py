#!/usr/bin/env python3
from __future__ import annotations

import collections
import dataclasses
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import Pos


@dataclasses.dataclass
class Map:
    walls: set[Pos]
    size: Pos
    start: Pos
    end: Pos

    @classmethod
    def parse(cls, lines_str: str) -> Map:
        walls = set()
        start = None
        end = None
        lines = lines_str.splitlines()
        size = Pos(len(lines), len(lines[0]))
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                pos = Pos(y, x)
                if c == "#":
                    walls.add(pos)
                elif c == "S":
                    start = pos
                elif c == "E":
                    end = pos
                else:
                    assert c == "."
        assert start
        assert end
        return cls(walls, size, start, end)

    def flood_fill(self, first_pos: Pos):
        queue = collections.deque([(first_pos, 0)])
        dist = {first_pos: 0}
        while queue:
            pos, steps = queue.popleft()
            for neighbor in pos.orthogonal_neighbors_sized(self.size):
                if neighbor in dist or neighbor in self.walls:
                    continue
                dist[neighbor] = steps + 1
                queue.append((neighbor, steps + 1))
        return dist

    def find_cheats(self):
        fwd = self.flood_fill(self.start)
        normal_time = fwd[self.end]
        print(f"{normal_time=}")

        back = self.flood_fill(self.end)
        cheats = []
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Pos(y, x)
                if pos not in self.walls:
                    continue
                for from_pos in pos.orthogonal_neighbors_sized(self.size):
                    if from_pos not in fwd:
                        continue
                    for to_pos in pos.orthogonal_neighbors_sized(self.size):
                        if to_pos not in back:
                            continue
                        if to_pos == from_pos:
                            continue
                        cheat_time = fwd[from_pos] + back[to_pos] + 2
                        if cheat_time >= normal_time:
                            continue
                        time_saved = normal_time - cheat_time
                        cheats.append((from_pos, to_pos, time_saved))
        return cheats


def main(p: pathlib.Path) -> None:
    map = Map.parse(p.read_text().strip())
    print(map)
    cheats = map.find_cheats()

    # Part 1.
    part1 = 0
    for _, _, time_saved in cheats:
        if time_saved >= 100:
            part1 += 1
    print(f"Part 1: {part1}")

    # by_time = {}
    # for _, _, time_saved in cheats:
    #     by_time.setdefault(time_saved, 0)
    #     by_time[time_saved] += 1
    # print(by_time)


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
