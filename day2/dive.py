#!/usr/bin/python

from typing import List
from enum import Enum
from dataclasses import dataclass

MINI = False

class Direction(Enum):
    """One-of 4 directions."""
    FORWARD = 1
    BACKWARD = 2
    UP = 3
    DOWN = 4

@dataclass
class Command:
    """Command for our ship."""
    direction: Direction
    amount: int

lines: List[str] = []
commands: List[Command] = []

def str2direction(direction: str) -> Direction:
    match direction:
        case "forward":
            return Direction.FORWARD
        case "backward":
            return Direction.BACKWARD
        case "up":
            return Direction.UP
        case "down":
            return Direction.DOWN


def parse_commands(lines: List[str]) -> List[Command]:
    """
    Parse lines from stdin (a text file, in this case) to commands.
    """
    cs: List[Direction] = []
    for line in lines:
        line = line.strip()
        direction, value = line.split(" ")
        cs.append(Command(str2direction(direction=direction), int(value)))
    return cs


with open("day2-mini.txt" if MINI else "day2.txt") as f:
    lines = f.readlines()

commands = parse_commands(lines)

# Compute sum

depth = 0
horiz = 0

for command in commands:
    match command.direction:
        case Direction.FORWARD:
            horiz += command.amount
        case Direction.DOWN:
            depth += command.amount
        case Direction.BACKWARD:
            horiz -= command.amount
        case Direction.UP:
            depth -= command.amount

new_depth = 0
new_horiz = 0
aim = 0

for command in commands:
    match command.direction:
        case Direction.FORWARD:
            new_horiz += command.amount
            new_depth += aim * command.amount
        case Direction.DOWN:
            aim += command.amount
        case Direction.BACKWARD:
            new_horiz -= command.amount
            new_depth -= aim * command.amount
        case Direction.UP:
            aim -= command.amount


print(f"{depth=}, {horiz=}, {depth * horiz=}")
print(f"{new_depth=}, {new_horiz=}, {aim=}, {new_depth * new_horiz=}")