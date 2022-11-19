#!/usr/bin/python

import math, copy
from typing import List, Optional, Tuple

MINI = True

lines: List[str] = []

with open("day3-mini.txt" if MINI else "day3.txt") as f:
    lines = f.readlines()


def parse_lines(lines: List[str]) -> Tuple[List[int], int]:
    vals: List[int] = []
    maximum: Optional[int] = None

    for line in lines:
        line = line.strip()
        line_b = int(line, 2)  # the second argument is the base!

        if maximum is None or line_b > maximum:
            maximum = line_b
        vals.append(line_b)

    return vals, maximum


def dth_bit(d: int, val: int) -> int:
    return 1 if val & (1 << d) else -1


vals, maximum = parse_lines(lines)

# Number of digits required to represent the maximum value in the list
num_digits = math.floor(math.log2(maximum)) + 1

counts = [0] * num_digits

# Runtime is O(N * D); there must be a binary trick to do it in O(N) but I don't see it
for val in vals:
    for d in range(num_digits):
        counts[d] += dth_bit(d, val)

# Determine gam, not it to create eps; multiply
gam = 0
for i, count in enumerate(counts):
    if count > 0:
        gam = gam | 1 << i

eps = ~gam & (2 ** num_digits - 1)

print(f"gam={gam}, eps={eps}, gam * eps={gam * eps}")


def create_counts(vals: List[int]) -> List[int]:
    maximum = max(vals)
    num_digits = math.floor(math.log2(maximum)) + 1

    counts = [0] * num_digits

    for val in vals:
        for d in range(num_digits):
            counts[d] += dth_bit(d, val)

    return counts


# Create oxygen generator rating, C02 scrubber rating with naive approach

oxygen_vals = copy.deepcopy(vals)
scrubber_vals = copy.deepcopy(vals)

idx = 0

while len(oxygen_vals) != 1:
    counts = create_counts(oxygen_vals)
    j = 0
    while j < len(oxygen_vals):
        oval = oxygen_vals[j]
        print(counts, idx, counts[idx], i, bin(oval), dth_bit(i, oval))
        if counts[idx] >= 0:
            if dth_bit(idx, oval) != 1:
                oxygen_vals.remove(oval)
                j = j - 1
        elif counts[idx] < 0:
            if dth_bit(idx, oval) != -1:
                oxygen_vals.remove(oval)
                j = j - 1
        j = j + 1
    idx += 1

print(f"counts={counts}")
for ov in oxygen_vals:
    print(bin(ov))

for sv in scrubber_vals:
    print(bin(sv))

print(f"oxygen_vals={oxygen_vals}")
print(f"scrubber_vals={scrubber_vals}")
print(f"result={oxygen_vals[0] * scrubber_vals[0]}")
