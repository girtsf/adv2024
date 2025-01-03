#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import DIRS_8, Pos

XMAS = "XMAS"


def part1_check_dir(lines: list[str], pos: Pos, dir: Pos) -> bool:
    size = Pos(len(lines), len(lines[0]))
    for i, c in enumerate(XMAS):
        if not pos.in_bounds(size):
            return False
        if lines[pos.y][pos.x] != c:
            return False
        pos += dir
    return True


def part1(lines: list[str]) -> int:
    count = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != "X":
                continue
            for dir in DIRS_8:
                if part1_check_dir(lines, Pos(y, x), dir):
                    count += 1
    return count


def part2(lines: list[str]) -> int:
    count = 0
    for y in range(1, len(lines) - 1):
        for x in range(1, len(lines[0]) - 1):
            if lines[y][x] != "A":
                continue
            if sorted([lines[y - 1][x - 1], lines[y + 1][x + 1]]) != ["M", "S"]:
                continue
            if sorted([lines[y - 1][x + 1], lines[y + 1][x - 1]]) != ["M", "S"]:
                continue
            count += 1
    return count


def main(p: pathlib.Path) -> None:
    lines = p.read_text().splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
