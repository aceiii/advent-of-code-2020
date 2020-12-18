#!/usr/bin/env python3

import sys
from enum import Enum
from collections import defaultdict



def is_active(state):
    return state == '#'


def cube_neighbours(pos):
    dimensions = len(pos)
    neighbours = set([(pos[0]+dx,) for dx in range(-1, 2)])
    for index in range(1, dimensions):
        new_neighbours = set()
        for diff in range(-1, 2):
            dim = pos[index] + diff
            for neighbour in neighbours:
                new_neighbours.add((*neighbour, dim))
        neighbours = new_neighbours
    neighbours.remove(pos)
    return neighbours


def parse_cubes(lines, dimensions=3):
    dimensions = max(3, dimensions)
    active_cubes = set()
    padding = [0] * (dimensions - 2)
    for y, line in enumerate(lines):
        for x, cube in enumerate(line.strip()):
            if is_active(cube):
                active_cubes.add(tuple([x, y] + padding))
                pass
    return active_cubes


class CubeSimulator:
    def __init__(self, active_cubes):
        self._active = active_cubes.copy()

    def step(self):
        counts = defaultdict(lambda: 0)
        new_actives = set()
        for active in self._active:
            for neighbour in cube_neighbours(active):
                counts[neighbour] += 1
        for active in self._active:
            if counts[active] == 2 or counts[active] == 3:
                new_actives.add(active)
        for cube, count in counts.items():
            if count == 3 and cube not in self._active:
                new_actives.add(cube)
        self._active = new_actives

    def run(self, cycles):
        for _ in range(cycles):
            self.step()

    def active_count(self):
        return len(self._active)


def part1(lines):
    cubes = parse_cubes(lines)
    sim = CubeSimulator(cubes)
    sim.run(6)
    return sim.active_count()


def part2(lines):
    cubes = parse_cubes(lines, 4)
    sim = CubeSimulator(cubes)
    sim.run(6)
    return sim.active_count()


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

