#!/usr/bin/env python3

import sys
import re
from enum import Enum
from operator import add, mul, sub


"""
ExpressionParser

expr        -> value ( op expr )* | "(" expr ")"
op          -> "+" | "*" | "-"
value       -> digit+
digit       -> "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

"""


ops = {
    "*": mul,
    "+": add,
    "-": sub,
}


class ExpressionParser:
    def __init__(self, line):
        self._chars = list(line)
        self._result = None
        self.parse()

    def __call__(self):
        return self.eval()

    def reset(self):
        self._index = -1
        self._level = 0
        self.next()

    def eval(self):
        return self._result() if callable(self._result) else None

    def peek(self):
        return "" if self._index >= len(self._chars) else self._chars[self._index]

    def accept(self, char):
        if self.peek() == char:
            self.next()
            return True
        return False

    def expect(self, chars):
        if self.peek() in chars:
            self.accept(self.peek())
            return True
        raise Exception("Found '{}', expecting {}".format(self.peek(), list(chars)))

    def next(self):
        while True:
            self._index += 1
            if self.peek() not in [" ", "\n", "\t"]:
                break

    def stmnt(self):
        expr = self.expr()
        while True:
            if self.peek() == ')':
                self.expect(')')
                self._level -= 1
            else:
                break
        if self._level > 0:
            raise Exception("Expecting ')'")
        if self.peek() != '':
            raise Exception('Unexpected character: {}'.format(self.peek()))
        return expr

    def expr(self):
        val1 = self.value()
        current_val = val1()

        while True:
            if self.peek() not in ops.keys():
                break

            op = self.op()
            val2 = self.value()
            current_val = op(current_val, val2())

        return lambda: current_val

    def op(self):
        c = self.peek()
        self.expect(ops.keys())
        return ops[c]

    def value(self):
        if self.peek() == '(':
            self.expect('(')
            expr = self.expr()
            self.expect(')')
            return expr

        digits = []
        while True:
            d = self.digit()
            if d is None:
                break
            digits.append(d)
        if not digits:
            raise Exception("Unexpected character: '{}'".format(self.peek()))
        value = int("".join(digits), 10)
        return lambda: value

    def digit(self):
        c = self.peek()
        match = re.match(r"[0-9]", c)
        if match is not None:
            self.accept(c)
            return match.group(0)
        return None

    def parse(self):
        try:
            self.reset()
            self._result = self.stmnt()
        except Exception as e:
            print(e)
            raise Exception("Error parsing: '{}'".format(''.join(self._chars)))

def parse_math(lines):
    return [ExpressionParser(line.strip()) for line in lines]


def part1(lines):
    expressions = parse_math(lines)
    return sum(exp() or 0 for exp in expressions)


def part2(lines):
    pass


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

