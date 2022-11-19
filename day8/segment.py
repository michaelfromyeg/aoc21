#!/usr/bin/python

from dataclasses import dataclass
from typing import Dict, Set, Tuple, List, Optional, Union
from pprint import PrettyPrinter

pp = PrettyPrinter()


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
    set("abcefg"),
    # 1 ... length 2 (unique)
    set("cf"),
    # 2 ... length 5
    set("acdeg"),
    # 3 ... length 5
    set("acdfg"),
    # 4 ... length 4 (unique)
    set("bcdf"),
    # 5 ... length 5
    set("abdfg"),
    # 6 ... length 6
    set("abdefg"),
    # 7 ... length 3 (unique)
    set("acf"),
    # 8 ... length 7 (unique)
    set("abcdefg"),
    # 9 ... length 6
    set("abcdfg"),
]

# Map unique lengths to their corresponding semgnets (will be handy!)
UNIQUE = {
    2: SEGMENTS[1],
    3: SEGMENTS[7],
    4: SEGMENTS[4],
    7: SEGMENTS[8],
}


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

    # problem 1; simply count the outputs that possess a unique length (1, 3, 4, and 7)
    count = 0
    for segment in segments:
        outputs = segment.outputs

        for o in outputs:
            s = o.size()
            if s == 2 or s == 4 or s == 3 or s == 7:
                count = count + 1

    # problem 2; now determine the full output
    s_sum = 0
    for segment in segments:
        s_map: Dict[str, Optional[Union[int, Set[int]]]] = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
            "f": None,
            "g": None,
        }

        inputs = segment.inputs
        outputs = segment.outputs

        ios = inputs.copy()
        ios.extend(outputs)

        # TODO: perform "process of elimination"
        #       logic here is currently backwards...
        for io in ios:
            s = io.size()
            if s in UNIQUE.keys():
                t = UNIQUE[s]
                for w in io.wires:
                    if s_map[w] is None:
                        s_map[w] = t
                    if len(s_map[w]) > 1:
                        s_map[w] = t.intersection(s_map[w])
                    if len(s_map[w]) == 1:
                        # Convert to single character
                        s_map[w] = "".join(s_map[w])

        pp.pprint(s_map)

    answer1 = count
    answer2 = -1

    return answer1, answer2


if __name__ == "__main__":
    mini: bool = True

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}, answer2={answer2}")
