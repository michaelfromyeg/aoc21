#!/usr/bin/python

from dataclasses import dataclass
from typing import Set, Tuple, List


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


@dataclass
class Wires:
    """
    A special string representing a combination of wires.
    """

    def __init__(self, wires) -> None:
        self.wires = set(wires)

    def __str__(self) -> str:
        """
        Return string representation of wires.
        """
        wires: str = "".join(self.wires)
        sorted_wires = "".join(sorted(wires, key=str.lower))
        return sorted_wires

    def size(self) -> int:
        return len(self.wires)

    wires: Set[str]


@dataclass
class Puzzle:
    """
    Representing a puzzle, a single line from our input.
    """

    inputs: List[Wires]
    outputs: List[Wires]

    def __repr__(self) -> str:
        """
        Print the puzzle in a nice way!
        """
        puzzle = ""

        puzzle += Color.BLUE
        inputs_str = [str(i) for i in self.inputs]
        puzzle += ", ".join(inputs_str)
        puzzle += Color.END

        puzzle += Color.BOLD + " >>> " + Color.END

        puzzle += Color.RED
        output_str = [str(o) for o in self.outputs]
        puzzle += ", ".join(output_str)
        puzzle += Color.END

        return puzzle


SEGMENTS = [
    # 0 ... length 6
    "abcefg",
    # 1 ... length 2 (unique)
    "cf",
    # 2 ... length 5
    "acdeg",
    # 3 ... length 5
    "acdfg",
    # 4 ... length 4 (unique)
    "bcdf",
    # 5 ... length 5
    "abdfg",
    # 6 ... length 6
    "abdefg",
    # 7 ... length 3 (unique)
    "acf",
    # 8 ... length 7 (unique)
    "abcdefg",
    # 9 ... length 6
    "abcdfg",
]


def read(mini: bool) -> List[Puzzle]:
    """
    Read in 7-segment display data.
    """
    lines: List[str] = []
    with open("./day8-mini.txt" if mini else "./day8.txt") as f:
        lines = f.readlines()

    puzzles: List[Puzzle] = []
    for line in lines:
        inputs, outputs = line.split(" | ")

        inputs = inputs.strip()
        outputs = outputs.strip()

        inputs = inputs.split(" ")
        outputs = outputs.split(" ")

        w_inputs = []
        w_outputs = []

        for i in inputs:
            i = i.strip()
            w_inputs.append(Wires(i))

        for o in outputs:
            o = o.strip()
            w_outputs.append(Wires(o))

        puzzles.append(Puzzle(w_inputs, w_outputs))

    for i, puzzle in enumerate(puzzles):
        print(f"{i}: {puzzle}")

    return puzzles


def solve(mini: bool) -> Tuple[int, int]:
    """
    See https://adventofcode.com/2021/day/8/.
    """
    segments = read(mini)

    count = 0

    for segment in segments:
        outputs = segment.outputs

        for output in outputs:
            if (
                output.size() == 2
                or output.size() == 4
                or output.size() == 3
                or output.size() == 7
            ):
                count = count + 1

    answer1 = count
    answer2 = -1

    return answer1, answer2


if __name__ == "__main__":
    mini: bool = False

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}, answer2={answer2}")
