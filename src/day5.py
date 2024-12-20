#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


def parse_order(order_str: str) -> dict[str, set[str]]:
    order = {}
    for line in order_str.splitlines():
        lhs, rhs = line.split("|")
        order.setdefault(lhs, set()).add(rhs)
        order.setdefault(rhs, set())
    return order


def parse_updates(pages_list_str: str) -> list[list[str]]:
    pages = []
    for page_str in pages_list_str.splitlines():
        pages.append(page_str.split(","))
    return pages


def filter_used_only(
    order: dict[str, set[str]], pages: list[str]
) -> dict[str, set[str]]:
    pages_set = set(pages)
    out = {}
    for p in pages:
        out[p] = {x for x in order[p] if x in pages_set}
    return out


def arrange(order: dict[str, set[str]], pages: list[str]) -> list[str]:
    order_this = filter_used_only(order, pages)

    out = []
    while len(out) < len(pages):
        k = next(k for k, v in order_this.items() if not v)
        out.append(k)
        del order_this[k]
        for v in order_this.values():
            v.discard(k)
    out.reverse()
    return out


def calculate(order: dict[str, set[str]], updates: list[list[str]], part2: bool) -> int:
    sum = 0
    for u in updates:
        pages = arrange(order, u)
        if (not part2 and pages == u) or (part2 and pages != u):
            mid = int(pages[len(pages) // 2])
            sum += mid
    return sum


def main(p: pathlib.Path) -> None:
    input = p.read_text().strip()
    order_str, updates_list_str = input.split("\n\n")
    order = parse_order(order_str)
    updates = parse_updates(updates_list_str)
    print(order)
    print(updates)
    print(calculate(order, updates, False))
    print(calculate(order, updates, True))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
