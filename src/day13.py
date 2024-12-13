#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import pathlib
import re
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
from lib import Pos


def parse_button(s: str, button: str) -> Pos:
    # Button A: X+94, Y+34
    m = re.search(r"(?m)^Button " + button + r": X\+(?P<x>\d+), Y\+(?P<y>\d+)$", s)
    if not m:
        raise ValueError(f"could not find button {button} in '{s}'")
    return Pos(int(m["y"]), int(m["x"]))


def parse_prize(s: str) -> Pos:
    # Prize: X=18641, Y=10279
    m = re.search(r"(?m)^Prize: X=(?P<x>\d+), Y=(?P<y>\d+)$", s)
    assert m
    return Pos(int(m["y"]), int(m["x"]))


@dataclasses.dataclass
class Machine:
    button_a: Pos
    button_b: Pos
    prize: Pos

    @classmethod
    def parse(cls, s: str) -> Machine:
        button_a = parse_button(s, "A")
        button_b = parse_button(s, "B")
        prize = parse_prize(s)
        return cls(button_a, button_b, prize)

    def find_presses(self, a_cost: int, b_cost: int) -> None | int:
        cheapest_cost = None
        for a in range(0, 101):
            for b in range(0, 101):
                x = self.button_a.x * a + self.button_b.x * b
                y = self.button_a.y * a + self.button_b.y * b
                pos = Pos(y, x)
                if pos != self.prize:
                    continue

                cost = a * a_cost + b * b_cost
                if cheapest_cost is None or cost < cheapest_cost:
                    cheapest_cost = cost

        return cheapest_cost

    def solve(self, a_cost: int, b_cost: int) -> None | int:
        # a * AX + b * BX = PX
        # a * AY + b * BY = PY
        #
        # a * AX = PX - b * BX
        # a = (PX - b * BX) / AX

        # (PX - b * BX) / AX * AY + b * BY = PY
        # PX * AY / AX - b * BX * AY / AX + b * BY = PY
        # b * BX * AY / AX - b * BY = PX * AY / AX - PY
        # b * (BX * AY / AX - BY) = PX * AY / AX - PY
        # b = (PX * AY / AX - PY) / (BX * AY / AX - BY)

        b = (self.prize.x * self.button_a.y / self.button_a.x - self.prize.y) / (
            self.button_b.x * self.button_a.y / self.button_a.x - self.button_b.y
        )
        a = (self.prize.x - b * self.button_b.x) / self.button_a.x

        b = round(b)
        a = round(a)
        if a * self.button_a.x + b * self.button_b.x != self.prize.x:
            return None
        if a * self.button_a.y + b * self.button_b.y != self.prize.y:
            return None

        return a * a_cost + b * b_cost


def check_machines(machines: list[Machine]) -> int:
    total_cost = 0
    for m in machines:
        if cost := m.solve(3, 1):
            total_cost += cost
    return total_cost


def main(p: pathlib.Path) -> None:
    input = p.read_text()
    machines = [Machine.parse(x) for x in input.split("\n\n")]

    part1 = check_machines(machines)
    print(f"part 1: {part1}")

    for m in machines:
        m.prize = Pos(m.prize.y + 10000000000000, m.prize.x + 10000000000000)

    part2 = check_machines(machines)
    print(f"part 2: {part2}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
