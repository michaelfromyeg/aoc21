#!/usr/bin/python

import math
from typing import List, Optional, Tuple

MINI = False


def solve():
    """
    See https://adventofcode.com/2021/day/3/.
    """
    lines: List[str] = []

    with open("day3-mini.txt" if MINI else "day3.txt") as f:
        lines = f.readlines()

    values, maximum = parse_lines(lines)

    # Number of digits required to represent the maximum value in the list
    num_digits = bits_needed(maximum)
    counts = [0] * num_digits

    # Runtime is O(N * D); there must be a binary trick to do it in O(N) but I don't see it
    for val in values:
        for d in range(num_digits):
            b = dth_bit(d, val)
            counts[d] += 1 if b == 1 else -1

    # Determine gam, not it to create eps; multiply
    gam = 0
    for i, count in enumerate(counts):
        if count > 0:
            gam = gam | 1 << i

    eps = ~gam & (2 ** num_digits - 1)

    print(f"gam={gam}, eps={eps}, gam * eps={gam * eps}")

    o2_rating = get_rating(values, num_digits, True)
    co2_rating = get_rating(values, num_digits, False)

    # print(co2_rating)

    print(
        f"o2_rating={o2_rating}, co2_rating={co2_rating}, product={o2_rating * co2_rating}"
    )


def parse_lines(lines: List[str]) -> Tuple[List[int], int]:
    """
    Parse a text file, also tracing it's maximum value.
    """

    values: List[int] = []
    maximum: Optional[int] = None

    for line in lines:
        line = line.strip()
        line_b = int(line, 2)  # the second argument is the base!

        if maximum is None or line_b > maximum:
            maximum = line_b
        values.append(line_b)

    return values, maximum


def dth_bit(d: int, val: int) -> int:
    """
    Return the dth bit of an integer.
    """
    # print(f"d={d}, val={bin(val)}, val_s={bin(val >> d)}, bit={(val >> d) & 1}")

    return (val >> d) & 1


def bits_needed(value: int) -> int:
    """
    Return the number of bits needed to represent an integer.
    """
    return math.floor(math.log2(value)) + 1


def majority_bit(values: List[int], d: int, direction: bool) -> int:
    """
    Return the majority bit of values at position d; either 0 or 1.
    """
    scores = [0, 0]
    for value in values:
        scores[dth_bit(d, value)] += 1

    # print(f"scores={scores}")

    # TODO: deal with tie-breaks
    if direction:
        return 0 if scores[0] > scores[1] else 1
    else:
        return 0 if scores[0] <= scores[1] else 1


def filter_values(values: List[int], d: int, majority: int) -> List[int]:
    """
    Filter down values.
    """
    new_values = []
    for value in values:
        if dth_bit(d, value) == majority:
            new_values.append(value)
    return new_values


def get_rating(values: List[int], num_digits: int, direction: bool) -> int:
    """
    Get the O2 rating.
    """
    d = num_digits if direction else num_digits - 1  # ???
    while len(values) != 1:
        majority = majority_bit(values, d, direction)
        # print(f"d={d}, majority={majority}")

        new_values = filter_values(values, d, majority)
        # print(f"new_values={new_values}")

        values = new_values
        d -= 1

        if d < 0:
            break

    if len(values) > 1:
        print(f"!! {values}")

    return values[0]


if __name__ == "__main__":
    solve()
