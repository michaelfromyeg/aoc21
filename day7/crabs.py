#!/usr/bin/python

from typing import Tuple, List


def read(mini: bool) -> List[int]:
    """
    Return crabs!

    (Very similar to day6.)
    """
    line: str = ""
    with open("./day7-mini.txt" if mini else "./day7.txt") as f:
        line = f.read()

    crabs = line.split(",")
    crabs = [int(crab) for crab in crabs]

    return crabs


def sum_to_n(n: int) -> int:
    """
    Use 'that' trick.
    """
    return (n * (n + 1)) // 2


def solve(mini: bool) -> Tuple[int, int]:
    """
    See https://adventofcode.com/2021/day/7/.
    """
    crabs = read(mini)

    # Gut: the "best" point is the median with this cost strategy
    crabs.sort()
    n = len(crabs)
    med_crab = crabs[n // 2]

    score = 0
    for crab in crabs:
        score += abs(med_crab - crab)

    answer1 = score

    # Gut: now we "weight" the moves; perhaps its the mean?
    # Unfortunately, this is wrong!

    # mean_crab = ceil(sum(crabs) / n)

    m_crab = min(crabs)
    min_score2 = float("inf")
    # min_m = m_crab

    while m_crab <= max(crabs):
        # print("m_crab", m_crab)

        score2 = 0
        for crab in crabs:
            gap = abs(m_crab - crab)
            score2 += sum_to_n(gap)

        if score2 < min_score2:
            min_score2 = score2
            # min_m = m_crab

        m_crab = m_crab + 1

    # print("min_m", min_m)

    answer2 = min_score2

    return answer1, answer2


if __name__ == "__main__":
    mini: bool = False

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}, answer2={answer2}")
