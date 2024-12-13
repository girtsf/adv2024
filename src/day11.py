#!/usr/bin/env python3

from __future__ import annotations

import pathlib
import sys


def rr(s: int, n: int, cache: dict) -> int:
    if n == 0:
        return 1
    if (s, n) in cache:
        return cache[(s, n)]

    if s == 0:
        out = rr(1, n - 1, cache)
    else:
        digits = str(s)
        if len(digits) % 2 == 0:
            s1 = int(digits[: len(digits) // 2], 10)
            s2 = int(digits[len(digits) // 2 :], 10)
            out = rr(s1, n - 1, cache) + rr(s2, n - 1, cache)
        else:
            out = rr(s * 2024, n - 1, cache)
    cache[(s, n)] = out
    return out


def r(stones: list[int], n: int) -> int:
    cache = {}
    return sum(rr(s, n, cache) for s in stones)


def main(p: pathlib.Path) -> None:
    stones = [int(x) for x in p.read_text().strip().split()]
    print(f"part 1: {r(stones, 25)}")
    print(f"part 2: {r(stones, 75)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
