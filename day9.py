#!/usr/bin/env python3

import sys


def find_invalid(numbers, preamble):
    valid_sets = [set() for _ in range(len(numbers))]
    for index, num in enumerate(numbers):
        for index2, num2 in enumerate(numbers[index+1:index+preamble]):
            if num != num2:
                valid_sets[index + index2 + 1].add(num + num2)


    valid_sets2 = []
    for index in range(len(numbers) - preamble):
        s = set().union(*valid_sets[index:index+preamble])
        valid_sets2.append(s)

    for index in range(preamble, len(numbers)):
        num = numbers[index]
        if num not in valid_sets2[index - preamble]:
            return num


def find_contiguous(numbers, target):
    lower = 0
    upper = 1
    current = numbers[0] + numbers[upper]
    while upper < len(numbers):
        if current == target:
            return numbers[lower:upper+1]
        if current < target:
            upper += 1
            current += numbers[upper]
        else:
            current -= numbers[lower]
            lower += 1


def part1(lines):
    preamble = 25
    numbers = [int(x, 10) for x in lines]
    return find_invalid(numbers, preamble)


def part2(lines):
    preamble = 25
    numbers = [int(x, 10) for x in lines]
    target = find_invalid(numbers, preamble)
    contiguous = sorted(find_contiguous(numbers, target))
    return contiguous[0] + contiguous[-1]


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

