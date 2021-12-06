#!/usr/bin/env python3

import sys
from enum import Enum
from collections import defaultdict


class RuleType(Enum):
    SUB = 0
    TERM = 1


def parse_rule(line):
    first, rest = line.split(": ", 1)
    rule_id = int(first.strip(), 10)
    if rest[0] == '"' and rest[-1] == '"':
        rule_type = RuleType.TERM
        args = (rest[1:-1],)
    else:
        rule_type = RuleType.SUB
        args = []
        parts = rest.split(" | ")
        for part in parts:
            args.append(tuple(int(i, 10) for i in part.split(" ")))
    return (rule_id, rule_type, args)


def term_func(rules, rule_id, args):
    def func(mesage, index=0, level=0):
        try:
            if mesage[index] == args[0]:
                return index + len(args[0])
        except:
            pass
        return None

    return func


def sub_func(rules, rule_id, args):
    def func(message, index=0, level=0):
        for sub_args in args:
            current = index
            for sub_rule_id in sub_args:
                next_index = rules[sub_rule_id](message, current, level+1)
                if next_index is None:
                    break
                current = next_index
            else:
                if level == 0 and message[current:] != '':
                    return None
                return current
    return func


def nil_func(message, index):
    return None


def compile_rules(rules):
    rulemap = defaultdict(lambda: nil_func)
    for rule in rules:
        rule_id, rule_type, args = rule
        if rule_type == RuleType.TERM:
            rulemap[rule_id] = term_func(rulemap, rule_id, args)
        else:
            rulemap[rule_id] = sub_func(rulemap, rule_id, args)

    return rulemap


def parse_input(lines):
    mode = 0
    rules = []
    messages = []
    for line in lines:
        line = line.strip()
        if line == '':
            mode += 1
            continue
        if mode == 0:
            rules.append(parse_rule(line))
            continue
        else:
            messages.append(line)

    return compile_rules(rules), messages


def check_rule(rule, message):
    index = rule(message, 0)
    if index is not None and message[index:] == '':
        return True
    return False


def part1(lines):
    rules, messages = parse_input(lines)
    passes = [m if rules[0](m) else None for m in messages]
    return sum(1 if p is not None else 0 for p in passes)


def part2(lines):
    rules, messages = parse_input(lines)
    rules[8] = sub_func(rules, 8, [(42,), (42, 8)])
    rules[11] = sub_func(rules, 11, [(42, 31), (42, 11, 31)])
    passes = [m if rules[0](m) else None for m in messages]
    return sum(1 if p is not None else 0 for p in passes)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

