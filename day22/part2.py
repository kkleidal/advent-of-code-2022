from part1 import *

def build_graph_cube(active_positions):
    positions = {k for k, v in active_positions.items() if v == EMPTY}

    pos, _ = initial_pos(active_positions)
    start_pos = pos
    side_length = max(p[1] for p in active_positions if p[0] == pos[0]) - pos[1] + 1

    rules = [
        (
            # Pairings 4 right and 6 top
            [
                (
                    (pos[0] + side_length + d, pos[1] + side_length - 1),
                    (pos[0] + 2 * side_length, pos[1] + 2 * side_length - d - 1)
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (1, 0), # crossing 4 to 6
            (0, -1), # crossing 6 to 4
        ),
        (
            # Pairings 1 right and 6 right
            [
                (
                    (pos[0] + d, pos[1] + side_length - 1),
                    (pos[0] + 3 * side_length - d - 1, pos[1] + 2 * side_length - 1)
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (0, -1), # crossing 1 to 6
            (0, -1), # crossing 6 to 1
        ),
        (
            # Pairings 2 left and 6 bottom
            [
                (
                    (pos[0] + side_length + d, pos[1] - 2 * side_length),
                    (pos[0] + 3 * side_length - 1, pos[1] + 2 * side_length - d - 1)
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (-1, 0), # crossing 2 to 6
            (0, 1), # crossing 6 to 2
        ),
        # Pairings 5 right and 6 left, unnecessary
        # Pairings 1 bottom and 4 top, unnecessary
        # Pairings 4 bottom and 5 top, unnecessary
        (
            # Pairings 2 bottom and 5 bottom
            [
                (
                    (pos[0] + 2 * side_length - 1, pos[1] - 2 * side_length + d),
                    (pos[0] + 3 * side_length - 1, pos[1] + side_length - d - 1),
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (-1, 0), # crossing 2 to 5
            (-1, 0), # crossing 5 to 2
        ),
        (
            # Pairings 1 top and 2 top
            [
                (
                    (pos[0], pos[1] + d),
                    (pos[0] + side_length, pos[1] - side_length - d - 1),
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (1, 0), # crossing 1 to 2
            (1, 0), # crossing 2 to 1
        ),
        # Pairings 3 right and 4 left, unnecessary
        # Pairings 3 left and 2 right, unnecessary
        (
            # Pairings 1 left and 3 top
            [
                (
                    (pos[0] + d, pos[1]),
                    (pos[0] + side_length, pos[1] - side_length + d),
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (1, 0), # crossing 1 to 3
            (0, 1), # crossing 3 to 1
        ),
        (
            # Pairings 3 bottom and 5 left
            [
                (
                    (pos[0] + 2 * side_length - 1, pos[1] - side_length + d),
                    (pos[0] + 3 * side_length - 1 - d, pos[1]),
                )
                for d in range(0, side_length)
            ],
            # Direction changes:
            (0, 1), # crossing 3 to 5
            (-1, 0), # crossing 5 to 3
        ),
        
    ]
    print(rules[0])
    special = defaultdict(dict)
    for rule in rules:
        for pairs in rule[0]:
            assert isinstance(pairs, tuple) and len(pairs) == 2
            assert all(isinstance(p, tuple) and len(p) == 2 for p in pairs)
            going = tuple(-1 * p for p in rule[2])
            special[pairs[0]][going] = (pairs[1], rule[1])
            assert isinstance(rule[1], tuple) and len(rule[1]) == 2
            going = tuple(-1 * p for p in rule[1])
            assert isinstance(rule[2], tuple) and len(rule[2]) == 2
            special[pairs[1]][going] = (pairs[0], rule[2])


    adjacency = defaultdict(dict)
    for pos in positions:
        # Up
        next_pos = (pos[0] - 1, pos[1])
        next_dir = (-1, 0)
        if next_pos not in active_positions:
            next_pos, next_dir = special[pos][next_dir]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(-1, 0)] = (next_pos, next_dir)

        # Down
        next_pos = (pos[0] + 1, pos[1])
        next_dir = (1, 0)
        if next_pos not in active_positions:
            next_pos, next_dir = special[pos][next_dir]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(1, 0)] = (next_pos, next_dir)

        # Right
        next_pos = (pos[0], pos[1] + 1)
        next_dir = (0, 1)
        if next_pos not in active_positions:
            print(special[pos])
            print(start_pos)
            print((pos[0] - start_pos[0], pos[1] - start_pos[1]))
            print(tuple(p / side_length for p in pos))
            next_pos, next_dir = special[pos][next_dir]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(0, 1)] = (next_pos, next_dir)

        # Left
        next_pos = (pos[0], pos[1] - 1)
        next_dir = (0, -1)
        if next_pos not in active_positions:
            next_pos, next_dir = special[pos][next_dir]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(0, -1)] = (next_pos, next_dir)
    return adjacency

def main():
    active_positions, instructions = parse()
    adjacency = build_graph_cube(active_positions)
    my_pos, my_dir = move(adjacency, *initial_pos(active_positions), instructions)
    return score(my_pos, my_dir)

if __name__ == '__main__':
    print(main())
