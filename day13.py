#!/usr/bin/env python3

import sys
from operator import itemgetter


def part1(lines):
    timestamp = int(lines[0].strip(), 10)
    buses = list(filter(lambda x: x != 'x', lines[1].strip().split(',')))
    ids = [int(x, 10) for x in buses]
    times = sorted([(i, i - (timestamp % i)) for i in ids], key=itemgetter(1))
    bus, wait = times[0]
    return bus * wait


def part2(lines):
    pass


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

