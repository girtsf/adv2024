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

    def find_cheats(self, cheat_time: int) -> dict[int, int]:
        fwd = self.flood_fill(self.start)
        back = self.flood_fill(self.end)
        assert back[self.start] == fwd[self.end]
        cheats_by_time_saved = collections.defaultdict(int)
        for y in range(self.size.y):
            for x in range(self.size.x):
                start_pos = Pos(y, x)
                if start_pos not in fwd:
                    continue

                for end_y in range(-cheat_time, cheat_time + 1):
                    for end_x in range(-cheat_time, cheat_time + 1):
                        steps = abs(end_y) + abs(end_x)
                        if steps > cheat_time:
                            continue
                        end_pos = start_pos + Pos(end_y, end_x)
                        if end_pos not in back:
                            continue
                        time_saved = fwd[self.end] - (
                            fwd[start_pos] + steps + back[end_pos]
                        )
                        if time_saved <= 0:
                            continue
                        cheats_by_time_saved[time_saved] += 1

        return cheats_by_time_saved

    def solve(self, cheat_time: int) -> int:
        cheats = self.find_cheats(cheat_time)
        # for t, count in sorted(cheats.items()):
        #     if t >= 50:
        #         print(f"{t=}, {count=}")
        return sum(v for k, v in cheats.items() if k >= 100)


def main(p: pathlib.Path) -> None:
    map = Map.parse(p.read_text().strip())
    print(f"part1: {map.solve(2)}")
    print(f"part2: {map.solve(20)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
