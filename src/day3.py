#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


def main(p: pathlib.Path) -> None:
    inp = p.read_text().strip()
    part1 = 0
    for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", inp):
        part1 += int(a) * int(b)
    print(part1)
    part2 = 0
    r = re.compile(r"(?P<op>do(n't)?\(\))|(mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\))")
    doin = True
    for m in r.finditer(inp):
        if m.group("op"):
            doin = m["op"] == "do()"
        elif doin:
            part2 += int(m["a"]) * int(m["b"])
    print(part2)


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
