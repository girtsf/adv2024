#!/usr/bin/env python3
from __future__ import annotations

import collections
import pathlib
import sys


def part1(conns: dict[str, set[str]]) -> int:
    out = set()
    for q in conns:
        for w in conns[q]:
            for e in conns[q]:
                if w == e:
                    continue
                if e not in conns[w]:
                    continue
                if q[0] != "t" and w[0] != "t" and e[0] != "t":
                    continue
                out.add(tuple(sorted([q, w, e])))
    return len(out)


# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bk(
    r: set[str], p: set[str], x: set[str], conns: dict[str, set[str]], out: set[str]
) -> None:
    if not p and not x:
        out.add(",".join(sorted(r)))
    for v in p.copy():
        bk(r.union({v}), p & conns[v], x & conns[v], conns, out)
        p.remove(v)
        x.add(v)


def part2(conns: dict[str, set[str]]) -> str:
    cliques = set()
    bk(set(), set(conns), set(), conns, cliques)
    max_len = max(len(x) for x in cliques)
    out = next(x for x in cliques if len(x) == max_len)
    return out


def main(p: pathlib.Path) -> None:
    conns = collections.defaultdict(set)
    for line in p.read_text().strip().splitlines():
        q, w = line.split("-")
        conns[q].add(w)
        conns[w].add(q)
    print(part1(conns))
    print(part2(conns))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
