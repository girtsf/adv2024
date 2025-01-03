#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import Pos


def find_antinodes(lines: list[str], lim: int) -> int:
    size = Pos(len(lines), len(lines[0]))
    antinodes = set()
    for y1 in range(len(lines)):
        for x1 in range(len(lines[0])):
            if lines[y1][x1] == ".":
                continue
            for y2 in range(len(lines)):
                for x2 in range(len(lines[0])):
                    if y2 < y1 or (y2 == y1 and x2 <= x1):
                        continue
                    if lines[y2][x2] != lines[y1][x1]:
                        continue
                    delta = Pos(y2 - y1, x2 - x1)
                    pos = Pos(y1, x1)
                    for _ in range(0, lim + 1):
                        antinodes.add(pos)
                        pos -= delta
                        if not pos.in_bounds(size):
                            break
                    pos = Pos(y2, x2)
                    for _ in range(0, lim + 1):
                        antinodes.add(pos)
                        pos += delta
                        if not pos.in_bounds(size):
                            break
    return len(antinodes)


def main(p: pathlib.Path) -> None:
    lines = p.read_text().splitlines()
    print(find_antinodes(lines, 1))
    print(find_antinodes(lines, 99999))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
