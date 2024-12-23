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
    blocks: list[Pos]
    exit: Pos
    size: Pos

    @classmethod
    def parse(cls, lines_str: str) -> Map:
        blocks = []
        for line in lines_str.splitlines():
            x, y = line.split(",")
            blocks.append(Pos(int(y), int(x)))
        max_y = max(p.y for p in blocks)
        max_x = max(p.x for p in blocks)
        exit = Pos(max_y, max_x)
        size = Pos(max_y + 1, max_x + 1)
        return cls(blocks, exit, size)

    def find_path(self, drop: int) -> None | int:
        w = set(self.blocks[:drop])
        start = Pos(0, 0)
        queue = collections.deque([(start, 0)])
        seen = {start}
        while queue:
            # print(f"{queue=}")
            pos, steps = queue.popleft()
            if pos == self.exit:
                return steps
            for neighbor in pos.orthogonal_neighbors_sized(self.size):
                if neighbor in w or neighbor in seen:
                    continue
                queue.append((neighbor, steps + 1))
                seen.add(neighbor)
        return None

    def part2(self) -> str:
        for i, b in enumerate(self.blocks, start=1):
            if not self.find_path(i):
                return f"{b.x},{b.y}"
        raise ValueError("No solution")


def main(p: pathlib.Path) -> None:
    map = Map.parse(p.read_text().strip())
    print(map.find_path(1024))
    print(map.part2())


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
