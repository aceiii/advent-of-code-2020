#!/usr/bin/env python3

import sys
import re
import traceback


def usage():
    print("usage: {} day [input]")
    exit(1)


def main():
    try:
        (day,) = re.match(r"^(\d+|day\d+)$", sys.argv[1]).groups()
        module = __import__("day{}".format(day))

        input_file = sys.argv[2] if len(sys.argv) > 2 else None

        if input_file is None:
            lines = sys.stdin.readlines()
        else:
            with open(input_file) as file:
                lines = file.readlines()

        has_part1 = hasattr(module, "part1")
        has_part2 = hasattr(module, "part2")

        if not has_part1 and not has_part2:
            print("Day{} has not been implemented".format(day))
            exit(1)

        if has_part1:
            try:
                print("Part1: {}".format(module.part1(lines)))
            except:
                print(traceback.format_exc())
                exit(1)

        if has_part2:
            try:
                print("Part2: {}".format(module.part2(lines)))
            except:
                print(traceback.format_exc())
                exit(1)

    except Exception as e:
        print(e)
        usage()


if __name__ == "__main__":
    main()

