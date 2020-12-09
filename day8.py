#!/usr/bin/env python3

import sys
from enum import Enum
from collections import defaultdict


class Op(Enum):
    ACC = "acc"
    JMP = "jmp"
    NOP = "nop"


class VM(object):
    def __init__(self, instructions):
        self._instructions = instructions
        self._iptr = 0
        self._accum = 0
        self._stop = False
        self._done = False
        self._iptrset = set()

    def _step(self, instruction):
        op, arg = instruction
        if op == Op.ACC:
            self._accum += arg
        elif op == Op.JMP:
            return arg
        return 1

    def step(self):
        stop_index = len(self._instructions)
        assert(self._iptr >= 0 and self._iptr <= stop_index)
        if self._iptr == stop_index:
            self._stop = True
            self._done = True
            return
        elif self._iptr in self._iptrset:
            self._stop = True
            return

        instruction = self._instructions[self._iptr]
        self._iptrset.add(self._iptr)
        self._iptr += self._step(instruction)

    def done(self):
        return self._done


    def run(self):
        while not self._stop:
            self.step()
        return self._accum


def parse_instruction(line):
    op, arg = line.strip().split(' ')
    return (Op(op), int(arg, 10))


def parse_boot_code(lines):
    return list(map(parse_instruction, lines))


def build_jump_graph2(instructions):
    jumps = []
    for index, instruction in enumerate(instructions):
        op, arg = instruction
        jump, swap = index + 1, None
        if op == Op.NOP:
            swap = index + arg
        elif op == Op.JMP:
            jump = index + arg
            swap = index + 1
        jumps.append((jump, swap))
    return jumps


class JumpNode(object):
    def __init__(self):
        self.prev = set()
        self.next = None
        self.alt_next = None

    def __repr__(self):
        return "prev:{}, next:{}, alt_next:{}".format(self.prev, self.next, self.alt_next)


def build_jump_graph(instructions):
    nodes = defaultdict(lambda: JumpNode())
    for index, instruction in enumerate(instructions):
        op, arg = instruction
        next_index = index + 1
        alt_next_index = None

        if op == Op.NOP:
            alt_next_index = index + arg
        elif op == Op.JMP:
            next_index = index + arg
            alt_next_index = index + 1

        nodes[index].next = next_index
        nodes[index].alt_next = alt_next_index
        nodes[next_index].prev.add(index)
    return nodes


def fix_instructions(instructions):
    jump_graph = build_jump_graph(instructions)
    target_index = len(instructions)
    last_node = jump_graph[target_index]
    while last_node:
        last_node = jump_graph[list(last_node.prev)[0]]


def part1(lines):
    instructions = parse_boot_code(lines)
    vm = VM(instructions)
    return vm.run()


def part2(lines):
    instructions = parse_boot_code(lines)
    for index, (op, arg) in enumerate(instructions):
        if op == Op.ACC:
            continue
        patch = instructions[:]
        patch[index] = (Op.JMP if op == Op.NOP else Op.NOP, arg)
        vm = VM(patch)
        res = vm.run()
        if vm.done():
            return res


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

