#!/usr/bin/python

from dataclasses import dataclass
from typing import List, Optional
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
class Point:
    """
    A point in 2D space.
    """

    x: int
    y: int

    def __hash__(self) -> int:
        x = self.x
        y = self.y

        # Use bijective algorithm described here
        # https://lsi.upc.edu/~alvarez/calculabilitat/enumerabilitat.pdf

        tmp = y + ((x + 1) // 2)
        return hash(x + tmp * tmp)


@dataclass
class Line:
    """
    A line with two coordinates.

    Either x1 = x2 or y1 = y2 indicates straightness. If not, is_hor is undefined (None).
    """

    def __init__(self, x1: int, x2: int, y1: int, y2: int) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.is_hor = self._is_hor()

    def _is_hor(self) -> Optional[bool]:
        """
        Determine whether a set of coordinates represent a horizontal line.
        """
        if self.x1 == self.x2:
            return True
        elif self.y1 == self.y2:
            return False
        return None

    # Coordinates of the line
    x1: int
    x2: int
    y1: int
    y2: int

    # Whether or not the line is horizontal
    is_hor: Optional[bool]

    def __repr__(self) -> str:
        """
        Return pretty string version of line.
        """
        coordinates = f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"
        if self.is_hor == True:
            coordinates = Color.BLUE + coordinates + Color.END
        elif self.is_hor == False:
            coordinates = Color.GREEN + coordinates + Color.END
        else:  # is_hor is None
            coordinates = Color.RED + coordinates + Color.END
        return coordinates


def read(mini: bool) -> List[Line]:
    """
    Read the puzzle input.
    """
    lines: List[str] = []
    with open("./day5-mini.txt" if mini else "./day5.txt") as f:
        lines = f.readlines()

    better_lines = []
    for line in lines:
        p1, p2 = line.split(" -> ")
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        better_lines.append(Line(x1, x2, y1, y2))

    return better_lines


def solve(mini: bool) -> int:
    """
    See https://adventofcode.com/2021/day/5/.
    """
    better_lines = read(mini)

    # Grid is a dict of points, since it's sparse (instead of 2D-matrix)
    grid = {}

    for better_line in better_lines:
        # Only process straight lines, for now
        if better_line.is_hor is not None:
            print(better_line)

            # if x1 == x2
            if better_line.is_hor == True:
                y = min(better_line.y1, better_line.y2)
                end = max(better_line.y1, better_line.y2)
                x = better_line.x1

                while y <= end:
                    if Point(x, y) in grid:
                        grid[Point(x, y)] += 1
                    else:
                        grid[Point(x, y)] = 1
                    y = y + 1

            # if y1 == y2
            if better_line.is_hor == False:
                x = min(better_line.x1, better_line.x2)
                end = max(better_line.x1, better_line.x2)
                y = better_line.y1

                while x <= end:
                    if Point(x, y) in grid:
                        grid[Point(x, y)] += 1
                    else:
                        grid[Point(x, y)] = 1
                    x = x + 1

    # pp.pprint(grid)

    values = grid.values()
    filtered_values = list(filter(lambda value: value >= 2, values))

    answer1 = len(filtered_values)

    # part 2; process diagonal lines too; only ever at angles of 45deg

    # Continue with the sparse representation
    complete_grid = {}

    for better_line in better_lines:
        # Same as before for horizontal, vertical
        if better_line.is_hor == True:
            y = min(better_line.y1, better_line.y2)
            end = max(better_line.y1, better_line.y2)
            x = better_line.x1

            while y <= end:
                if Point(x, y) in complete_grid:
                    complete_grid[Point(x, y)] += 1
                else:
                    complete_grid[Point(x, y)] = 1
                y = y + 1
        elif better_line.is_hor == False:
            x = min(better_line.x1, better_line.x2)
            end = max(better_line.x1, better_line.x2)
            y = better_line.y1

            while x <= end:
                if Point(x, y) in complete_grid:
                    complete_grid[Point(x, y)] += 1
                else:
                    complete_grid[Point(x, y)] = 1
                x = x + 1
        else:  # diagonal lines; this is new!
            # Our goal is to find the leftmost point of the line and iterate
            x1 = better_line.x1
            x2 = better_line.x2
            y1 = better_line.y1
            y2 = better_line.y2

            p_leftmost = Point(x1, y1) if x1 < x2 else Point(x2, y2)
            p_other = Point(x1, y1) if x1 >= x2 else Point(x2, y2)

            # From the leftmost point, should we go UP (and right) or DOWN (and right)
            direction = 1 if p_leftmost.y < p_other.y else -1

            x = p_leftmost.x
            y = p_leftmost.y
            end = p_other.x

            while x <= end:
                if Point(x, y) in complete_grid:
                    complete_grid[Point(x, y)] += 1
                else:
                    complete_grid[Point(x, y)] = 1

                # Move up OR down along the diagonal
                x = x + 1
                y = y + direction

    values = complete_grid.values()
    filtered_values = list(filter(lambda value: value >= 2, values))

    answer2 = len(filtered_values)

    return answer1, answer2


if __name__ == "__main__":
    mini: bool = False

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}, answer2={answer2}")
