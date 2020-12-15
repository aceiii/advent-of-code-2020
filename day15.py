#!/usr/bin/env python3

import sys


def parse_numbers(lines):
    return [int(x, 10) for x in lines[0].strip().split(',')]


def play_number_game(numbers, target):
    number_index = {}
    last_spoken = (None, False, 0)
    for index, num in enumerate(numbers):
        last_spoken = (num, num not in number_index, 0)
        number_index[num] = index
    for index in range(len(numbers), target):
        last_num, is_first, diff = last_spoken
        if is_first:
            num = 0
        else:
            num = diff
        last_spoken = (
            num,
            num not in number_index,
            index-number_index[num] if num in number_index else 0
        )
        number_index[num] = index
    return last_spoken[0]


def part1(lines):
    numbers = parse_numbers(lines)
    target = 2020
    return play_number_game(numbers, target)


def part2(lines):
    numbers = parse_numbers(lines)
    target = 30000000
    return play_number_game(numbers, target)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

