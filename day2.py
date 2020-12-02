#!/usr/bin/env python3

import sys
import re


def parse_line(line):
    groups = re.match(r"(\d+)-(\d+) ([a-z]): (.*)", line).groups()
    (num1, num2, char, password) = groups
    return (((int(num1, 10), int(num2, 10)), char), password)


def validate_line(rule, password):
    (min_count, max_count), char = rule
    count = password.count(char)
    return count >= min_count and count <= max_count


def validate_line2(rule, password):
    (index1, index2), char = rule
    match1 = password[index1-1] == char
    match2 = password[index2-1] == char
    return match1 ^ match2


def part1(lines):
    parsed_lines = map(parse_line, lines)
    valid_lines = filter(lambda line: validate_line(*line), parsed_lines)
    return len(list(valid_lines))


def part2(lines):
    parsed_lines = map(parse_line, lines)
    valid_lines = filter(lambda line: validate_line2(*line), parsed_lines)
    return len(list(valid_lines))


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

