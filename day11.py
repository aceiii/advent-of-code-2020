#!/usr/bin/env python3

import sys
from enum import Enum


class Seating(Enum):
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'


def is_floor(c):
    return c == Seating.FLOOR


def is_empty(c):
    return c == Seating.EMPTY


def is_occupied(c):
    return c == Seating.OCCUPIED


def count_occupied(seats):
    return sum(sum(1 if is_occupied(c) else 0 for c in row) for row in seats)


def seats_equal(seats1, seats2):
    return all(map(lambda x: all(map(lambda y: y[0] == y[1],  list(zip(*x)))), zip(seats1, seats2)))


def parse_seat_row(row):
    return [Seating(c) for c in row.strip()]


def parse_seats(lines):
    return [parse_seat_row(line) for line in lines]


def get_seat(seats, pos):
    x, y = pos
    return seats[y][x]


def is_out_of_bounds(pos, bounds):
    x, y = pos
    width, height = bounds
    return x < 0 or x >= width or y < 0 or y >= height


def get_neighbours(seats, pos):
    x, y = pos
    bounds = (len(seats[0]), len(seats))
    adjacent = [(0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    neighbours = []
    for adj_x, adj_y in adjacent:
        pos = x + adj_x, y + adj_y
        if is_out_of_bounds(pos, bounds):
            continue
        neighbours.append(get_seat(seats, pos))
    return neighbours


def model_seat_change(seats, pos):
    seat = get_seat(seats, pos)
    neighbours = get_neighbours(seats, pos)
    occupied = sum(1 if is_occupied(n) else 0 for n in neighbours)
    if is_empty(seat) and occupied == 0:
        return Seating.OCCUPIED
    elif is_occupied(seat) and occupied >= 4:
        return Seating.EMPTY
    return seat


def simulate_passengers(seats):
    new_seats = []
    steps = 0
    while True:
        steps += 1
        print("steps: {}".format(steps))
        for row_index, row in enumerate(seats):
            new_row = []
            for index, seat in enumerate(row):
                new_row.append(model_seat_change(seats, (index, row_index)))
            new_seats.append(new_row)
        if seats_equal(seats, new_seats):
            return new_seats
        seats = new_seats


class SeatNode:
    def __init__(self, pos):
        self.pos = pos
        self.seating = Seating.FLOOR
        self.next_seating = Seating.FLOOR
        self.neighbours = set()

    def __repr__(self):
        neighbours = [n.pos for n in self.neighbours]
        return "SeatNode{}:{} => [{}]".format(self.pos, self.seating, neighbours)

    def is_floor(self):
        return is_floor(self.seating)

    def is_empty(self):
        return is_empty(self.seating)

    def is_occupied(self):
        return is_occupied(self.seating)

    def update(self):
        if self.is_floor():
            return

        occupied = sum(1 if n.is_occupied() else 0 for n in self.neighbours)
        if self.is_empty() and occupied == 0:
            self.next_seating = Seating.OCCUPIED
        elif self.is_occupied() and occupied >= 4:
            self.next_seating = Seating.EMPTY

    def commit(self):
        if self.seating == self.next_seating:
            return False
        self.seating = self.next_seating
        return True


class SeatSimulator:
    def __init__(self, seats):
        self._height = len(seats)
        self._width = len(seats[0])
        self._seats = {}

        for row_index, row in enumerate(seats):
            for index, seat in enumerate(row):
                pos = (index, row_index)
                if pos not in self._seats:
                    self._seats[pos] = SeatNode(pos)
                nodeA = self._seats[pos]
                nodeA.seating = seat
                for npos in self._neighbours(pos):
                    if npos not in self._seats:
                        self._seats[npos] = SeatNode(npos)
                    nodeB = self._seats[npos]
                    nodeB.neighbours.add(nodeA)
                    nodeA.neighbours.add(nodeB)

    def _neighbours(self, pos):
        x, y = pos
        w, h = self._width, self._height
        adjacent = [(0, -1), (1, -1), (1, 0), (1, 1),
                    (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        neighbours = [(x + ax, y + ay) for ax, ay in adjacent]
        return [n for n in neighbours if not is_out_of_bounds(n, (w, h))]


    def _update(self):
        for seat in self._seats.values():
            seat.update()

    def _commit(self):
        changed = 0
        for seat in self._seats.values():
            changed += 1 if seat.commit() else 0
        return changed

    def run(self):
        step_count = 0
        while True:
            step_count += 1
            self._update()
            if self._commit() == 0:
                return step_count

    def occupied(self):
        return sum(1 if s.is_occupied() else 0 for s in self._seats.values())

    def __repr__(self):
        lines = []
        for y in range(self._height):
            row = []
            for x in range(self._width):
                pos = (x, y)
                row.append(self._seats[pos].seating.value)
            lines.append(''.join(row))
        lines.append("\n")
        return '\n'.join(lines)


class SeatNodeAdvanced:
    def __init__(self, pos):
        self.pos = pos
        self.seating = Seating.FLOOR
        self.next_seating = Seating.FLOOR
        self.neighbours = set()

    def __repr__(self):
        neighbours = []
        node = list(self.neighbours)[1]
        while node:
            neighbours.append(node.node.pos)
            node = node.next
        return "SeatNodeAdvanced{}:{} => [{}]".format(self.pos, self.seating, neighbours)

    def is_floor(self):
        return is_floor(self.seating)

    def is_empty(self):
        return is_empty(self.seating)

    def is_occupied(self):
        return is_occupied(self.seating)

    def occupied_neighbours(self):
        count = 0
        for neighbour in self.neighbours:
            while neighbour:
                node = neighbour.node
                if node.is_occupied():
                    count += 1
                    break
                neighbour = neighbour.next
        return count

    def update(self):
        if self.is_floor():
            return

        occupied = self.occupied_neighbours()
        if self.is_empty() and occupied == 0:
            self.next_seating = Seating.OCCUPIED
        elif self.is_occupied() and occupied >= 5:
            self.next_seating = Seating.EMPTY

    def commit(self):
        if self.seating == self.next_seating:
            return False
        self.seating = self.next_seating
        return True

class NeighbourNode:
    def __init__(self, node):
        self.node = node
        self.next = None


class SeatSimulatorAdvanced:
    def __init__(self, seats):
        self._height = len(seats)
        self._width = len(seats[0])
        self._seats = {}

        adjacent = [(0, -1), (1, -1), (1, 0), (1, 1),
                    (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        bounds = (self._width, self._height)

        for y, row in enumerate(seats):
            for x, seat in enumerate(row):
                pos = (x, y)
                node = SeatNodeAdvanced(pos)
                node.seating = seat
                self._seats[pos] = node

        for y, row in enumerate(seats):
            for x, seat in enumerate(row):
                pos = (x, y)
                parent = self._seats[pos]
                for nx, ny in adjacent:
                    prev = None
                    npos = (x + nx, y + ny)
                    while not is_out_of_bounds(npos, bounds):
                        node = self._seats[npos]
                        neighbour = NeighbourNode(node)
                        if prev is None:
                            parent.neighbours.add(neighbour)
                        else:
                            prev.next = neighbour
                        prev = neighbour
                        npos = (npos[0] + nx, npos[1] + ny)

                        if not node.is_floor():
                            break

    def _update(self):
        for seat in self._seats.values():
            seat.update()

    def _commit(self):
        changed = 0
        for seat in self._seats.values():
            changed += 1 if seat.commit() else 0
        return changed

    def run(self, debug=False):
        step_count = 0
        while True:
            step_count += 1
            if debug:
                print("step {}:".format(step_count))
                print(self)
            self._update()
            if self._commit() == 0:
                return step_count

    def occupied(self):
        return sum(1 if s.is_occupied() else 0 for s in self._seats.values())

    def __repr__(self):
        lines = []
        for y in range(self._height):
            row = []
            for x in range(self._width):
                pos = (x, y)
                row.append(self._seats[pos].seating.value)
            lines.append(''.join(row))
        lines.append("\n")
        return '\n'.join(lines)


def part1(lines):
    seats = parse_seats(lines)
    sim = SeatSimulator(seats)
    sim.run()
    return sim.occupied()


def part2(lines):
    seats = parse_seats(lines)
    sim = SeatSimulatorAdvanced(seats)
    sim.run()
    return sim.occupied()


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

