#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


def r(result: int, so_far: int, numbers: list[int], part2: bool) -> bool:
    if not numbers:
        return so_far == result
    if r(result, so_far + numbers[0], numbers[1:], part2):
        return True
    if r(result, so_far * numbers[0], numbers[1:], part2):
        return True
    if part2 and r(result, int(str(so_far) + str(numbers[0])), numbers[1:], part2):
        return True
    return False


def solve_one(line: str, part2: bool) -> int:
    res_str, numbers_str = line.split(": ")
    res = int(res_str)
    numbers = [int(x) for x in numbers_str.split(" ")]
    if r(res, numbers[0], numbers[1:], part2):
        return res
    return 0


def solve_all(lines: list[str], part2: bool) -> int:
    return sum(solve_one(line, part2) for line in lines)


def main(p: pathlib.Path) -> None:
    lines = p.read_text().splitlines()
    print(solve_all(lines, False))
    print(solve_all(lines, True))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
