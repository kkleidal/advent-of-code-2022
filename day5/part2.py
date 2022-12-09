import sys
from collections import deque
import re
from dataclasses import dataclass
from part1 import parse

if __name__ == "__main__":
    towers, commands = parse()
    for command in commands:
        vals = [towers[command.source].pop() for _ in range(command.count)]
        for val in vals[::-1]:
            towers[command.dest].append(val)

    print("".join(tower.pop() for tower in towers))
