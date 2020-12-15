#!/usr/bin/env python3

import sys


def find_pairs(numbers, target):
    prev_numbers = set()
    for number in numbers:
        diff = target - number
        if diff in prev_numbers:
            return (number, diff)
        prev_numbers.add(number)
    raise ValueError("target {} not found".format(target))


def find_triplets(numbers, target):
    pairs = dict()
    for i in range(0, len(numbers)):
        for j in range(i+1, len(numbers)):
            num1 = numbers[i]
            num2 = numbers[j]
            pairs[num1 + num2] = (num1, num2)
    for number in numbers:
        diff = target - number
        if diff in pairs:
            (num1, num2) = pairs[diff]
            return (number, num1, num2)
    raise ValueError("target {} not found".format(target))


def part1(lines):
    numbers = [int(x, 10) for x in lines]
    (num1, num2) = find_pairs(numbers, 2020)
    return num1 * num2


def part2(lines):
    numbers = [int(x, 10) for x in lines]
    (num1, num2, num3) = find_triplets(numbers, 2020)
    return num1 * num2 * num3


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

