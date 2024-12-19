#!/usr/bin/env python3
from __future__ import annotations

import collections
import pathlib
import sys


def ways_to_make(design: str, towels: list[str]) -> int:
    ways = collections.defaultdict(int)
    ways[0] = 1
    for pos in range(len(design)):
        if pos not in ways:
            continue
        for towel in towels:
            if design[pos : pos + len(towel)] == towel:
                ways[pos + len(towel)] += ways[pos]

    return ways[len(design)]


def part1(have: list[str], want: list[str]) -> int:
    return sum(1 if ways_to_make(x, have) else 0 for x in want)


def part2(have: list[str], want: list[str]) -> int:
    return sum(ways_to_make(x, have) for x in want)


def main(p: pathlib.Path) -> None:
    input = p.read_text().strip()
    have_str, want_str = input.split("\n\n")
    have = have_str.split(", ")
    want = want_str.split("\n")
    print(f"part1: {part1(have, want)}")
    print(f"part2: {part2(have, want)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
