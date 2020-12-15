#!/usr/bin/env python3

import sys
from enum import Enum

class Instr(Enum):
    MASK = 1
    MEM = 2


def parse_mask(mask):
    mask1 = int('0b' + mask.replace('X', '0'), 2)
    mask2 = int('0b' + mask.replace('X', '1'), 2)

    def mask_func(value):
        return (value | mask1) & mask2

    return mask_func

def parse_loc_mask(mask):
    mask_val = int('0b' + mask.replace('X', '0'), 2)
    bits = [i for i, x in enumerate(mask) if x == 'X']

    def mask_func(value):
        addrs = []
        base = "{:036b}".format(value | mask_val)
        for num in range(2**len(bits)):
            binary = ("{:0" + str(len(bits)) + "b}").format(num)
            ones = list(base)
            for index, bit in enumerate(bits):
                ones[bit] = binary[index]
            addr = ''.join(ones)
            addrs.append(addr)
        return addrs

    return mask_func


def parse_line(line):
    left, right = line.strip().split(' = ')
    if left == 'mask':
        return (Instr.MASK, parse_mask(right))

    loc = int(left[4:-1], 10)
    value = int(right, 10)
    return (Instr.MEM, (loc, value))


def parse_line2(line):
    left, right = line.strip().split(' = ')
    if left == 'mask':
        return (Instr.MASK, parse_loc_mask(right))

    loc = int(left[4:-1], 10)
    value = int(right, 10)
    return (Instr.MEM, (loc, value))

def parse_program(lines):
    return [parse_line(line) for line in lines]

def parse_program2(lines):
    return [parse_line2(line) for line in lines]


def part1(lines):
    program = parse_program(lines)
    memory = {}
    mask = lambda x: x
    for instr, op in program:
        if instr == Instr.MASK:
            mask = op
        else:
            loc, value = op
            memory[loc] = mask(value)
    return sum(value for value in memory.values())


def part2(lines):
    program = parse_program2(lines)
    memory = {}
    mask = lambda x: [x]
    for instr, op in program:
        if instr == Instr.MASK:
            mask = op
        else:
            orig_loc, value = op
            for loc in mask(orig_loc):
                memory[loc] = value
    return sum(value for value in memory.values())

def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

