#!/usr/bin/python

from typing import List, Optional
from dataclasses import dataclass


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
class Tile:
    """
    A tile.
    """

    value: int
    marked: bool


@dataclass
class Board:
    """
    A game board.
    """

    tiles: List[List[Tile]]

    def _row_marked(self, i):
        """
        Determine if a row is fully marked.
        """
        row = self.tiles[i]

        return all(r.marked for r in row)

    def _col_marked(self, j):
        """
        Determine if a column is fully marked.
        """
        col = []
        for row in self.tiles:
            col.append(row[j])

        return all(c.marked for c in col)

    def is_solved(self) -> bool:
        """
        Determine if the board is solved.
        """
        # Check rows
        for i in range(len(self.tiles)):
            if self._row_marked(i):
                return True

        # Check columns
        for j in range(len(self.tiles[0])):
            if self._col_marked(j):
                return True

        # Diagonals don't count, so we're done
        return False

    def mark(self, value) -> None:
        """
        Blot the bingo sheet.
        """
        for row in self.tiles:
            for cell in row:
                if cell.value == value:
                    cell.marked = True

    def score(self) -> int:
        """
        Get the board's score.
        """
        score = 0
        for row in self.tiles:
            for cell in row:
                if not cell.marked:
                    score += cell.value
        return score

    def __repr__(self) -> str:
        """
        For pretty printing!
        """
        s = ""

        for row in self.tiles:
            values = []
            for cell in row:
                value = str(cell.value)

                # Add leading 0 so always 2-digits
                if cell.value < 10:
                    value = "0" + value

                # Bold if Tile is marked
                if cell.marked:
                    value = Color.YELLOW + value + Color.END

                values.append(value)

            row_s = ", ".join(values)
            s += row_s + "\n"
        return s


def solve(mini: bool) -> int:
    """
    See https://adventofcode.com/2021/day/4/.
    """
    bingo_numbers, boards = read(mini)

    if mini:
        print("== NUMBERS ==")
        print(bingo_numbers)

        print()

        for board in boards:
            print("== BOARD ==")
            print(board)

    best_board: Optional[Board] = None
    idx = 0
    while not best_board:
        bingo_number = bingo_numbers[idx]

        for board in boards:
            board.mark(bingo_number)
            if board.is_solved():
                print(f"Solved!,\n{board}\n")
                best_board = board

        if best_board == None:
            idx = idx + 1

    best_score = best_board.score()
    last_called = bingo_numbers[idx]
    answer1 = best_score * last_called

    # print(f"best_score={best_score}, last_called={last_called}")
    # print(f"product={best_score * last_called}")

    # part 2; get last board!
    last_board: Optional[Board] = None
    solved_boards = []
    idx = 0

    while not last_board:
        bingo_number = bingo_numbers[idx]

        for i, board in enumerate(boards):
            board.mark(bingo_number)
            if i not in solved_boards and board.is_solved():
                solved_boards.append(i)

                if len(solved_boards) == len(boards):
                    print(f"Solved!,\n{board}\n")
                    last_board = board

        if last_board == None:
            idx = idx + 1

    last_score = last_board.score()
    last_called = bingo_numbers[idx]
    answer2 = last_score * last_called

    return answer1, answer2


# TODO: add return type
def read(mini: bool):
    """
    Read in puzzle input.
    """
    lines: List[str] = []
    with open("./day4-mini.txt" if mini else "./day4.txt") as f:
        lines = f.read()

    chunks = lines.split("\n\n")

    bingo_numbers = parse_bingo_numbers(chunks[0])

    chunks = chunks[1:]
    boards = parse_boards(chunks)

    return bingo_numbers, boards


def parse_bingo_numbers(s) -> List[int]:
    """
    Get bingo numbers.
    """
    return [int(x) for x in s.split(",")]


def parse_boards(chunks) -> List[Board]:
    boards = []
    for chunk in chunks:
        boards.append(parse_board(chunk))
    return boards


def parse_board(chunk) -> Board:
    """
    Parse the board.
    """
    tiles = []
    lines = chunk.split("\n")

    for line in lines:
        row = []
        values = line.split()

        for value in values:
            value = value.strip()
            value = int(value)
            row.append(Tile(value=value, marked=False))

        tiles.append(row)

    return Board(tiles=tiles)


if __name__ == "__main__":
    mini: bool = False

    answer1, answer2 = solve(mini)

    print(f"answer1={answer1}")
    print(f"answer2={answer2}")
