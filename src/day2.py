#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


def is_safe(report: list[int]) -> bool:
    if report[0] < report[1]:
        ascending = True
    else:
        ascending = False
    prev = report[0]
    for x in report[1:]:
        delta = abs(x - prev)
        if delta < 1 or delta > 3:
            return False
        if ascending and x < prev:
            return False
        if not ascending and x > prev:
            return False
        prev = x
    return True


def parse_line(s: str) -> list[int]:
    return [int(i) for i in s.split()]


def is_safe_or_fixable(report: list[int]) -> int:
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1 :]):
            return True
    return False


def main(p: pathlib.Path) -> None:
    reports = [parse_line(x) for x in p.read_text().strip().splitlines()]
    part1 = sum(is_safe(report) for report in reports)
    print(part1)
    part2 = sum(is_safe_or_fixable(report) for report in reports)
    print(part2)


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
