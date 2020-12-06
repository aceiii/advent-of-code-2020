#!/usr/bin/env python3

import sys
from functools import reduce
from collections import defaultdict


def parse_declarations(lines):
    declarations = []
    declaration = defaultdict(lambda: 0)
    persons = 0
    for line in lines:
        line = line.strip()
        if line == '':
            declarations.append((persons, declaration))
            declaration = defaultdict(lambda: 0)
            persons = 0
            continue
        persons += 1
        for char in line.strip():
            declaration[char] += 1
    declarations.append((persons, declaration))
    return declarations


def part1(lines):
    declarations = parse_declarations(lines)
    return sum(len(declaration.keys()) for _, declaration in declarations)


def part2(lines):
    declarations = parse_declarations(lines)
    count_match = lambda x, y: sum(1 if count == x else 0 for _, count in y.items())
    return sum(count_match(*declaration) for declaration in declarations)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

