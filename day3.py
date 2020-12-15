#!/usr/bin/env python3

import sys
from functools import reduce


def is_tree(tile):
    return tile == "#"


class TreeMap(object):
    def __init__(self, lines):
        self.lines = [line.strip() for line in lines]
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def at(self, pos):
        x, y = pos
        if y > self.height:
            raise IndexError("Invalid y position: {}".format(y))
        return self.lines[y][x % self.width]


def count_trees(tree_map, slope):
    pos = (0, 0)
    trees = 0
    while pos[1] < tree_map.height:
        if is_tree(tree_map.at(pos)):
            trees += 1
        pos = tuple(map(sum, zip(pos, slope)))
    return trees


def part1(lines):
    tree_map = TreeMap(lines)
    slope = (3, 1)
    return count_trees(tree_map, slope)


def part2(lines):
    tree_map = TreeMap(lines)
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    trees = [count_trees(tree_map, slope) for slope in slopes]
    return reduce(lambda a,b: a*b, trees)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

