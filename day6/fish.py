#!/usr/bin/python

from typing import List, Tuple


class Color:
    """
    Terminal colors enum.
    """

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def read(mini: bool) -> List[int]:
    """
    Return fishes; each is a Poisson process (HA!)
    """
    line: str = ""
    with open("./day6-mini.txt" if mini else "./day6.txt") as f:
        line = f.read()

    fishes = line.split(",")
    fishes = [int(fish) for fish in fishes]

    return fishes


def solve(mini: bool) -> Tuple[int, int]:
    """
    See https://adventofcode.com/2021/day/6/.
    """

    fishes = read(mini)
    # print(f"fishes={fishes}")

    days: int = 80

    for day in range(days):
        new_fishes = []
        for fish in fishes:
            new_fish = fish - 1
            if new_fish == -1:
                new_fishes.append(6)
                new_fishes.append(8)
            else:
                new_fishes.append(new_fish)
        fishes = new_fishes

    answer1 = len(fishes)

    # part 2; re-do where days=256
    # naive approach doesn't work anymore; gets terribly slow
    # use map instead of array (lol)

    fishes = read(mini)
    fishes_map = {}

    for idx in range(0, 9):
        fishes_map[idx] = 0
    for fish in fishes:
        fishes_map[fish] += 1

    days = 256

    for day in range(days):
        # print(fishes_map)

        m_0 = fishes_map[0]
        m_1 = fishes_map[1]
        m_2 = fishes_map[2]
        m_3 = fishes_map[3]
        m_4 = fishes_map[4]
        m_5 = fishes_map[5]
        m_6 = fishes_map[6]
        m_7 = fishes_map[7]
        m_8 = fishes_map[8]

        fishes_map[0] = m_1
        fishes_map[1] = m_2
        fishes_map[2] = m_3
        fishes_map[3] = m_4
        fishes_map[4] = m_5
        fishes_map[5] = m_6
        fishes_map[6] = m_7 + m_0
        fishes_map[7] = m_8
        fishes_map[8] = m_0

    values = fishes_map.values()
    answer2 = sum(values)

    return answer1, answer2


if __name__ == "__main__":
    mini: bool = False

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}, answer2={answer2}")
