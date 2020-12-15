#!/usr/bin/env python3

import sys
from enum import Enum


def turn(facing, direction):
    directions = ['N', 'E', 'S', 'W']
    index = directions.index(facing)
    return directions[(index + (1 if direction == 'R' else -1)) % 4]


def turn_point(pos, direction):
    x, y = pos
    if direction == 'L':
        return (y, -x)
    else:
        return (-y, x)


def move(facing, value):
    if facing == 'N':
        return (0, -value)
    elif facing == 'S':
        return (0, value)
    elif facing == 'E':
        return (value, 0)
    else:
        return (-value, 0)


def parse_navigation(lines):
    return [(x[0], int(x.strip()[1:], 10)) for x in lines]


def navigate(instructions):
    pos = (0, 0)
    facing = 'E'
    for action, value in instructions:
        x, y = pos
        if action == 'L' or action == 'R':
            turns = int(value / 90)
            while turns > 0:
                turns -= 1
                facing = turn(facing, action)
        else:
            mx, my = move(facing if action == 'F' else action, value)
            pos = (x + mx, y + my)
    return pos


def navigate_waypoint(instructions):
    pos = (0, 0)
    waypoint = (10, -1)
    for action, value in instructions:
        x, y = pos
        wx, wy = waypoint
        if action == 'L' or action == 'R':
            turns = int(value / 90)
            while turns > 0:
                turns -= 1
                waypoint = turn_point(waypoint, action)
        elif action == 'F':
            pos = (x + (wx * value), y + (wy * value))
        else:
            mx, my = move(action, value)
            waypoint = (wx + mx, wy + my)
    return pos


def part1(lines):
    instructions = parse_navigation(lines)
    x, y = navigate(instructions)
    return abs(x) + abs(y)


def part2(lines):
    instructions = parse_navigation(lines)
    x, y = navigate_waypoint(instructions)
    return abs(x) + abs(y)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

