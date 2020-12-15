#!/usr/bin/env python3

import sys
from operator import itemgetter


def parse_schedule(lines):
    timestamp = int(lines[0].strip(), 10)
    schedule = lines[1].strip().split(',')
    buses = [(int(x, 10), i) for i, x in enumerate(schedule) if x != 'x']
    return (timestamp, buses)


def match_buses(ts, buses):
    return all((ts + index) % bus == 0 for bus, index in buses)


def part1(lines):
    timestamp, buses = parse_schedule(lines)
    ids = [x for x, _ in buses]
    times = sorted([(i, i - (timestamp % i)) for i in ids], key=itemgetter(1))
    bus, wait = times[0]
    return bus * wait


def find_timestamp(start, inc, bus1, bus2):
    n = start
    id1, offset1 = bus1
    id2, offset2 = bus2
    while True:
        if (n + offset1) % id1 == 0 and (n + offset2) % id2 == 0:
            return n
        n += inc


def find_offset_increment(start, inc, bus1, bus2):
    ts1 = find_timestamp(start, inc, bus1, bus2)
    ts2 = find_timestamp(ts1 + inc, inc, bus1, bus2)
    return ts1, ts2 - ts1


def part2(lines):
    _, buses = parse_schedule(lines)
    offset, inc = 0, 1
    for index, bus1 in enumerate(buses[:-1]):
        bus2 = buses[index+1]
        offset, inc = find_offset_increment(offset+inc, inc, bus1, bus2)
        if match_buses(offset, buses):
            return offset


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

