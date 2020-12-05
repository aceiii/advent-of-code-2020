#!/usr/bin/env python3

import sys


def parse_boarding_pass(line):
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(line[7:10].replace('L', '0').replace('R', '1'), 2)
    return ((row * 8) + col, (row, col))


def parse_passes(lines):
    return [parse_boarding_pass(line.strip()) for line in lines]


def part1(lines):
    passes = parse_passes(lines)
    return max(seat_id for seat_id, _ in passes)


def part2(lines):
    passes = parse_passes(lines)
    seat_ids = sorted(seat_id for seat_id, _ in passes)
    first = seat_ids[0]
    last = seat_ids[-1]
    for index, seat_id in enumerate(range(first, last)):
        if seat_ids[index] != seat_id:
            return seat_id


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

