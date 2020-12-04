#!/usr/bin/env python3

import sys


def parse_passport(lines):
    passport = {}
    for line in lines:
        for field in line.strip().split(' '):
            key, value = field.split(':')
            passport[key] = value
    return passport


def parse_passport_batch(lines):
    passports = []
    passport_lines = []
    for line in lines:
        if line.strip() == '':
            passports.append(parse_passport(passport_lines))
            passport_lines = []
            continue
        passport_lines.append(line)
    else:
        passports.append(parse_passport(passport_lines))
    return passports


required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

def has_required_fields(passport):
    missing = required_fields.difference(passport.keys())
    return len(missing) == 0


def validate_byr(value):
    year = int(value, 10)
    return year >= 1920 and year <= 2002


def validate_iyr(value):
    year = int(value, 10)
    return year >= 2010 and year <= 2020


def validate_eyr(value):
    year = int(value, 10)
    return year >= 2020 and year <= 2030


def validate_hgt(value):
    unit = value[-2:]
    height = int(value[:-2], 10)
    if unit == 'cm':
        return height >= 150 and height <= 193
    elif unit == 'in':
        return height >= 59 and height <= 76
    return False


def validate_hcl(value):
    pound = value[0]
    colour = int(value[1:], 16)
    return pound == '#' and colour is not None


def validate_ecl(value):
    colours = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
    return value in colours


def validate_pid(value):
    number = int(value, 10)
    return len(value) == 9 and number is not None


def validate_cid(value):
    return True


field_validators = {
    'byr': validate_byr,
    'iyr': validate_iyr,
    'eyr': validate_eyr,
    'hgt': validate_hgt,
    'hcl': validate_hcl,
    'ecl': validate_ecl,
    'pid': validate_pid,
    'cid': validate_cid,
}


def validate_field(key, value):
    try:
        validate = field_validators[key]
        return validate(value)
    except:
        return False


def validate_passport(passport):
    if not has_required_fields(passport):
        return False
    return all([validate_field(key, value) for key, value in passport.items()])


def part1(lines):
    passports = parse_passport_batch(lines)
    return len(list(filter(has_required_fields, passports)))


def part2(lines):
    passports = parse_passport_batch(lines)
    return len(list(filter(validate_passport, passports)))


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

