#!/usr/bin/env python3

import sys
from operator import mul
from functools import reduce


def parse_rule_range(line):
    low, high = [int(x, 10) for x in line.split('-')]

    def rule(val):
       return val >= low and val <= high

    return rule


def parse_rule(line):
    name, rest = line.split(': ', 1)
    rules = [parse_rule_range(r) for r in rest.split(' or ')]

    def validate(val):
        return any(rule(val) for rule in rules)

    return (name, validate)


def parse_ticket(line):
    return tuple(int(x, 10) for x in line.split(','))


def parse_input(lines):
    mode = 0
    rules = []
    tickets = []
    for line in lines:
        line = line.strip()
        if line == '':
            mode += 1
            continue
        elif line == 'your ticket:' or line == 'nearby tickets:':
            continue

        if mode == 0:
            rules.append(parse_rule(line))
        elif mode >= 1:
            tickets.append(parse_ticket(line))
    return rules, tickets


def validate_field(rules, val):
    return any(rule(val) for _, rule in rules)


def validate_ticket(rules, ticket):
    return all(validate_field(rules, val) for val in ticket)


def invalid_fields(rules, ticket):
    invalid = []
    for field in ticket:
        if not validate_field(rules, field):
            invalid.append(field)
    return invalid


def calculate_scanning_error_rate(rules, tickets):
    invalid = []
    for ticket in tickets:
        invalid.extend(invalid_fields(rules, ticket))
    return sum(invalid)


def resolve_fields(rules, tickets):
    fields = {}
    transposed = list(zip(*tickets))

    for field, rule in rules:
        indexes = set()
        for index, vals in enumerate(transposed):
            if all(rule(val) for val in vals):
                indexes.add(index)
        fields[field] = indexes

    found = set()
    while True:
        singles = [(f, list(i)[0]) for f, i in fields.items() if len(i) == 1 and f not in found]
        if len(singles) == 0:
            break

        for field, index in singles:
            found.add(field)
            for key in fields.keys():
                if key == field:
                    continue
                if index in fields[key]:
                    fields[key].remove(index)

    return {f: i.pop() for f, i in fields.items()}


def part1(lines):
    rules, tickets = parse_input(lines)
    return calculate_scanning_error_rate(rules, tickets[1:])


def part2(lines):
    rules, tickets = parse_input(lines)
    my_ticket = tickets[0]
    valid_tickets = [t for t in tickets[1:] if validate_ticket(rules, t)]
    fields = resolve_fields(rules, valid_tickets)
    departure_fields = [(f, i) for f, i in fields.items() if "departure" in f]
    return reduce(mul, [my_ticket[i] for _, i in departure_fields])


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

