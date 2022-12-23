import sys
from collections import defaultdict

EMPTY = '.'
WALL = '#'

def parse():
    state = 0
    active_positions = {}
    instructions = []
    for i, line in enumerate(sys.stdin):
        line = line.rstrip()
        if line:
            if state == 0:
                for j, c in enumerate(line):
                    if c in (EMPTY, WALL):
                        active_positions[(i, j)] = c
            elif state == 1:
                pending_int = None
                for c in line:
                    if c.isdigit():
                        if pending_int is None:
                            pending_int = 0
                        pending_int = pending_int * 10 + int(c)
                    else:
                        if pending_int is not None:
                            instructions.append(pending_int)
                            pending_int = None
                        direction = c
                        instructions.append(direction)
                if pending_int is not None:
                    instructions.append(pending_int)
                    pending_int = None
            else:
                assert False
        else:
            state += 1
    return active_positions, instructions

def build_graph(active_positions):
    # Make graph:
    positions = {k for k, v in active_positions.items() if v == EMPTY}
    adjacency = defaultdict(dict)
    for pos in positions:
        # Up
        next_pos = (pos[0] - 1, pos[1])
        if next_pos not in active_positions:
            next_pos = (max(posi[0] for posi in active_positions if posi[1] == pos[1]), pos[1])
        if active_positions[next_pos] == EMPTY:
            adjacency[pos][(-1, 0)] = (next_pos, None)

        # Down
        next_pos = (pos[0] + 1, pos[1])
        if next_pos not in active_positions:
            next_pos = (min(posi[0] for posi in active_positions if posi[1] == pos[1]), pos[1])
        if active_positions[next_pos] == EMPTY:
            adjacency[pos][(1, 0)] = (next_pos, None)

        # Right
        next_pos = (pos[0], pos[1] + 1)
        if next_pos not in active_positions:
            next_pos = (pos[0], min(posi[1] for posi in active_positions if posi[0] == pos[0]))
        if active_positions[next_pos] == EMPTY:
            adjacency[pos][(0, 1)] = (next_pos, None)

        # Left
        next_pos = (pos[0], pos[1] - 1)
        if next_pos not in active_positions:
            next_pos = (pos[0], max(posi[1] for posi in active_positions if posi[0] == pos[0]))
        if active_positions[next_pos] == EMPTY:
            adjacency[pos][(0, -1)] = (next_pos, None)
    return adjacency

def turn(my_dir, instruction):
    if instruction == "L":
        return (-1 * my_dir[1], my_dir[0])
    else:
        assert instruction == "R"
        return (my_dir[1], -1 * my_dir[0])

def initial_pos(active_positions):
    my_y = min(pos[0] for pos, v in active_positions.items() if v == EMPTY)
    my_x = min(pos[1] for pos, v in active_positions.items() if v == EMPTY and pos[0] == my_y)
    my_pos = (my_y, my_x)
    my_dir = (0, 1)
    return my_pos, my_dir

def move(adjacency, my_pos, my_dir, instructions):
    for instruction in instructions:
        # print(instruction)
        if isinstance(instruction, int):
            for _ in range(instruction):
                neighbors = adjacency[my_pos]
                if my_dir in neighbors:
                    # print("MOVE", my_pos, neighbors[my_dir], active_positions[neighbors[my_dir]])
                    my_pos, dir_change = neighbors[my_dir]
                    if dir_change is not None:
                        assert isinstance(dir_change, tuple) and len(dir_change) == 2
                        my_dir = dir_change
        else:
            my_dir = turn(my_dir, instruction)
        # print(my_pos, my_dir, adjacency[my_pos])
    return my_pos, my_dir

def score(my_pos, my_dir):
    row = my_pos[0] + 1
    col = my_pos[1] + 1
    facing_score = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }[my_dir]
    return 1000 * row + 4 * col + facing_score

def main():
    active_positions, instructions = parse()
    adjacency = build_graph(active_positions)
    my_pos, my_dir = move(adjacency, *initial_pos(active_positions), instructions)
    return score(my_pos, my_dir)

if __name__ == '__main__':
    print(main())
