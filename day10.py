#!/usr/bin/env python3

import sys
from collections import defaultdict


def part1(lines):
    jolts = sorted(list(map(lambda x: int(x, 10), lines)))
    diffs = defaultdict(lambda: 0)
    for index in range(1, len(jolts)):
        jolt1 = jolts[index-1]
        jolt2 = jolts[index]
        diff = jolt2 - jolt1
        diffs[diff] += 1
    return (diffs[3] + 1) * (diffs[1] + 1)


def part2(lines):
    pass


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

