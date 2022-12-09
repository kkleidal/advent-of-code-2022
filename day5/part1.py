import sys
from collections import deque
import re
from dataclasses import dataclass


@dataclass
class MoveCommand:
    count: int
    source: int
    dest: int


def parse():
    state = 0
    towers = None
    pat = re.compile("^move (\d+) from (\d+) to (\d+)$")
    commands = []
    for line in sys.stdin:
        if state == 0:
            if "[" in line:
                # 4n-1=len
                # n = (len+1)/4
                if towers is None:
                    line = line.strip("\n")
                    n_towers = (len(line) + 1) // 4
                    towers = [deque() for _ in range(n_towers)]
                for tower_i, i in enumerate(range(0, len(line), 4)):
                    part = line[i:i+4].strip()
                    if part:
                        towers[tower_i].appendleft(part[1:-1])
            elif line.strip():
                ... # numbers
            else:
                # blank line
                state += 1
        elif state == 1:
            line = line.strip()
            m = pat.match(line)
            if m:
                commands.append(MoveCommand(
                    count=int(m.group(1)),
                    source=int(m.group(2)) - 1,
                    dest=int(m.group(3)) - 1,
                ))
    return towers, commands
                

if __name__ == "__main__":
    towers, commands = parse()
    for command in commands:
        for _ in range(command.count):
            val = towers[command.source].pop()
            towers[command.dest].append(val)

    print("".join(tower.pop() for tower in towers))
