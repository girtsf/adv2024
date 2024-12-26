#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import pathlib
import sys


def parse_inputs(inputs: str) -> dict[str, bool]:
    out = {}
    for line in inputs.splitlines():
        k, v = line.split(": ")
        out[k] = v == "1"
    return out


@dataclasses.dataclass
class Gate:
    inputs: tuple[str, str]
    op: str
    output: str

    @classmethod
    def parse(cls, text: str) -> Gate:
        lhs, output = text.split(" -> ")
        in1, op, in2 = lhs.split()
        return cls((in1, in2), op, output)

    def do(self, in1: bool, in2: bool) -> bool:
        if self.op == "AND":
            return in1 and in2
        elif self.op == "OR":
            return in1 or in2
        elif self.op == "XOR":
            return in1 != in2
        else:
            raise ValueError(f"Unknown op: {self.op}")


def calc_z(wires: dict[str, bool]) -> int:
    out = 0
    for k, v in wires.items():
        if not k.startswith("z"):
            continue
        if not v:
            continue
        out |= 1 << int(k[1:])
    return out


def propagate(inputs: dict[str, bool], gates: list[Gate]) -> int:
    wires = inputs.copy()
    progress = True
    while progress:
        progress = False
        gates2 = []
        for g in gates:
            if g.inputs[0] in wires and g.inputs[1] in wires:
                wires[g.output] = g.do(wires[g.inputs[0]], wires[g.inputs[1]])
                progress = True
            else:
                gates2.append(g)
        gates = gates2
    return calc_z(wires)


def main(p: pathlib.Path) -> None:
    text = p.read_text().strip()
    inputs_str, gates_str = text.split("\n\n")
    inputs = parse_inputs(inputs_str)
    gates = [Gate.parse(x) for x in gates_str.splitlines()]
    print(propagate(inputs, gates))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
