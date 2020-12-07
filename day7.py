#!/usr/bin/env python3

import sys
from collections import defaultdict


def parse_rule(line):
    color_part, rule_part = line.strip('.').split(' contain ')
    color_name = color_part[:-5]
    rule = {}
    if rule_part != 'no other bags':
        for rule_section in rule_part.split(', '):
            num, rest = rule_section.split(' ', 1)
            count = int(num, 10)
            color = rest[:-5 if count > 1 else -4]
            rule[color] = int(num, 10)
    return (color_name, rule)


def parse_rules(lines):
    rules = {}
    for line in lines:
        color, rule = parse_rule(line.strip())
        rules[color] = rule
    return rules


def reverse_rules(rules):
    rev_rules = defaultdict(lambda: set())
    for color, rule in rules.items():
        for contained_color in rule.keys():
            rev_rules[contained_color].add(color)
    return rev_rules


def count_bags(rules, target):
    items = rules[target].items()
    return sum(cnt + (cnt * count_bags(rules, col)) for col, cnt in items)


def part1(lines):
    bags = set()
    queue = []
    target = "shiny gold"

    rules = parse_rules(lines)
    rev_rules = reverse_rules(rules)

    for color in rev_rules[target]:
        queue.append(color)
        bags.add(color)

    while len(queue):
        contained_color = queue.pop()
        for color in rev_rules[contained_color]:
            if color not in bags:
                bags.add(color)
                queue.append(color)

    return len(bags)


def part2(lines):
    target = "shiny gold"
    rules = parse_rules(lines)
    count = count_bags(rules, target)
    return count


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

