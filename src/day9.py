#!/usr/bin/env python3
from __future__ import annotations

import collections
import dataclasses
import pathlib
import sys


@dataclasses.dataclass
class File:
    size: int
    file_idx: int


@dataclasses.dataclass
class Space:
    size: int


def grab_right_block(data: collections.deque[File | Space]) -> None | int:
    while data:
        match data.pop():
            case Space(_):
                continue
            case File(size, file_idx):
                if size > 1:
                    data.append(File(size - 1, file_idx))
                return file_idx
    return None


def grab_first_file_from_right(
    data: collections.deque[File | Space], max_size: int
) -> None | File:
    i = len(data) - 1
    while i >= 0:
        res = data[i]
        match res:
            case Space(_):
                pass
            case File(size, _):
                if size <= max_size:
                    del data[i]
                    return res
        i -= 1
    return None


def part1(input: list[File | Space]) -> int:
    data = collections.deque(input)
    checksum = 0
    idx = 0
    file_id = 0
    while data:
        item = data.popleft()
        # print(f"{idx=} {item=} {data=}")
        match item:
            case File(size, file_id):
                for _ in range(size):
                    checksum += idx * file_id
                    idx += 1
                file_id += 1
            case Space(size):
                for _ in range(size):
                    file_id = grab_right_block(data)
                    if file_id is not None:
                        checksum += idx * file_id
                        pass
                    idx += 1
    return checksum


def part2(input: list[File | Space]) -> int:
    idx = 0
    blocks = {}
    spaces = collections.defaultdict(list)
    for item in input:
        match item:
            case File(size, _):
                blocks[idx] = item
                idx += size
            case Space(size):
                spaces[size].append(idx)
                idx += size

    def find_first_space(size_needed: int, max_idx: int) -> None | int:
        smallest_idx = None
        smallest_size = None
        for size in range(size_needed, 10):
            if size not in spaces:
                continue
            if not spaces[size]:
                continue
            first_idx = spaces[size][0]
            if first_idx >= max_idx:
                continue
            if smallest_idx is None or first_idx < smallest_idx:
                smallest_idx = first_idx
                smallest_size = size
        if smallest_idx is not None:
            assert smallest_size
            spaces[smallest_size].pop(0)
            remains = smallest_size - size_needed
            if remains:
                spaces[remains].append(smallest_idx + size_needed)
                spaces[remains].sort()

            return smallest_idx
        else:
            return None

    input = input.copy()
    hi_idx = max(blocks.keys())
    checksum = 0
    for idx in range(hi_idx, -1, -1):
        block = blocks.get(idx)
        if not block:
            continue
        maybe_space = find_first_space(block.size, idx)
        if maybe_space is not None:
            for i in range(block.size):
                checksum += (maybe_space + i) * block.file_idx
        else:
            for i in range(block.size):
                checksum += (idx + i) * block.file_idx

    return checksum


def parse(input: str) -> list[File | Space]:
    out = []
    file_idx = 0
    for i, c in enumerate(input):
        size = int(c)
        if not size:
            continue
        if i % 2 == 0:
            assert size > 0
            out.append(File(size, file_idx))
            file_idx += 1
        else:
            out.append(Space(size))
    return out


def main(p: pathlib.Path) -> None:
    input = parse(p.read_text().strip())
    print(f"part 1: {part1(input)}")
    print(f"part 2: {part2(input)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
