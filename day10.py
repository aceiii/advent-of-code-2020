#!/usr/bin/env python3

import sys
from collections import defaultdict


def parse_jolts(lines):
    return sorted(list(map(lambda x: int(x.strip(), 10), lines)))


def part1(lines):
    jolts = parse_jolts(lines)
    diffs = defaultdict(lambda: 0)
    for index in range(1, len(jolts)):
        jolt1 = jolts[index-1]
        jolt2 = jolts[index]
        diff = jolt2 - jolt1
        diffs[diff] += 1
    return (diffs[3] + 1) * (diffs[1] + 1)


def part2(lines):
    jolts = parse_jolts(lines)
    jolts.insert(0, 0)
    jolts.append(jolts[-1] + 3)
    combos = {jolts[-1]: 1}
    for n in range(len(jolts)-2, -1, -1):
        jolt = jolts[n]
        adapters = list(filter(lambda x: x <= jolt+3, jolts[n+1:n+4]))
        combos[jolt] = sum(combos[i] for i in adapters)
    return combos[0]


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

