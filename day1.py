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


def part1(numbers, target):
    (num1, num2) = find_pairs(numbers, target)
    answer = num1 * num2
    print("Part1: {}".format(answer))


def part2(numbers, target):
    (num1, num2, num3) = find_triplets(numbers, target)
    answer = num1 * num2 * num3
    print("Part2: {}".format(answer))


def main():
    target = 2020
    numbers = list(map(lambda x: int(x, 10), sys.stdin.readlines()))
    part1(numbers, target)
    part2(numbers, target)


if __name__ == "__main__":
    main()

