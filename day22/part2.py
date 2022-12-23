from part1 import *

def only_one(lst):
    els = list(lst)
    assert len(els) == 1
    return els[0]

def build_graph_cube(active_positions):
    # FOLD CUBE

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    edge = set()
    for pos in active_positions:
        neighbors = sum(1 if (pos[0] + d[0], pos[1] + d[1]) in active_positions else 0 for d in directions)
        if neighbors < 4:
            edge.add(pos)
    start_point = min(edge)
    direction = (0, 1)
    next_point = (start_point[0] + direction[0], start_point[1] + direction[1])
    assert next_point in edge
    edge_ordered = [start_point, next_point]
    cur_point = next_point
    diags = set()
    while cur_point != start_point:
        next_point = (cur_point[0] + direction[0], cur_point[1] + direction[1])
        if next_point in edge:
            ...
        elif next_point in active_positions:
            # diag
            found = False
            for dy in range(-1, 2):
                if found:
                    break
                for dx in range(-1, 2):
                    pt = (cur_point[0] + dy, cur_point[1] + dx)
                    if (dy, dx) != (0, 0) and pt not in edge_ordered and pt in edge:
                        direction = (pt[0] - next_point[0], pt[1] - next_point[1])
                        next_point = pt
                        diags.add((cur_point, next_point))
                        found = True
                        break
            assert next_point in edge
        else:
            for new_dir_inst in ["R", "L"]:
                new_dir = turn(direction, new_dir_inst)
                next_point = (cur_point[0] + new_dir[0], cur_point[1] + new_dir[1])
                if next_point in edge:
                    direction = new_dir
                    break
            assert next_point in edge
        edge_ordered.append(next_point)
        cur_point = next_point
    edge_ordered = edge_ordered[:-1]

    orientations = [{
        d
        for d in directions
        if (cur_point[0] + d[0], cur_point[1] + d[1]) not in active_positions
    } for cur_point in edge_ordered]

    links = {}

    N = len(edge_ordered)
    for d1, d2 in diags:
        # print("ZIP", d1, d2)
        d1p = edge_ordered.index(d1)
        d2p = edge_ordered.index(d2)
        o1 = only_one(orientations[d1p])
        o2 = only_one(orientations[d2p])
        while True:
            d1p_pos = edge_ordered[d1p]
            d2p_pos = edge_ordered[d2p]
            # print("LINK", d1p_pos, d2p_pos)
            links[(d1p_pos, o1)] = (d2p_pos, tuple(-x for x in o2))
            links[(d2p_pos, o2)] = (d1p_pos, tuple(-x for x in o1))
            if len(orientations[d1p]) > 1 or len(orientations[d2p]) > 1: # corner
                break
            d1p = (d1p - 1) % N
            d2p = (d2p + 1) % N
    
    # ZIP: 4r with 6t
    # ZIP: 5l with 3b
    # ZIP: 1l with 3t
    
    # ROUNDS:
    # (0, 8), (4, 3): 1t with 2t
    # (8, 15), (3, 11): 6r with 1r
    # (11, 8), (7, 3): 5b with 2b
    # (7, 0), (11, 12): 2l with 6b
    while True:
        # print("=========")
        # print("New round")
        # print("=========")
        edge_with_orientation = {(p, o) for p, os in zip(edge_ordered, orientations) for o in os}
        edge_not_linked = edge_with_orientation - set(links)
        possible_link_locations = {p for p, _ in edge_not_linked} & {p for p, _ in links}
        possible_link_locations = {
            p for p in possible_link_locations
            if not (
                # don't match corner to corner; we'll lose all volume
                len(orientations[edge_ordered.index(p)]) == 2
                and len(orientations[edge_ordered.index(only_one(
                    p2 for (p1, _), (p2, _) in links.items()
                    if p1 == p
                ))]) == 2
            )
        }
        # print("Possible:", possible_link_locations)
        if not possible_link_locations:
            break
        d1 = min(possible_link_locations)
        _, o1 = only_one((p, o) for p, o in edge_not_linked if p == d1)
        _, d2, o2_alt = only_one((o, p2, o2) for (p1, o), (p2, o2) in links.items() if p1 == d1 and o != o1)

        d1p = edge_ordered.index(d1)
        if o1 in orientations[(d1p + 1) % N]:
            d1p_delta = 1
        else:
            d1p_delta = -1
        assert (edge_ordered[d1p], o1) not in links
        assert (edge_ordered[(d1p + d1p_delta) % N], o1) not in links

        orientations_at_d2 = orientations[edge_ordered.index(d2)]
        avail_orient_at_d2 = orientations_at_d2 - orientations_at_d2
        if len(avail_orient_at_d2) == 0:
            # flat edge, make fold
            # print("flat edge")
            d2p = edge_ordered.index(d2)
            d2p_delta = 1 if not any(p == edge_ordered[(d2p + 1) % N] for p, _ in links) else -1
            d2p += d2p_delta
            o2 = only_one(orientations[d2p] & orientations[d2p + d2p_delta])
            
            assert (edge_ordered[d2p], o2) not in links
            assert (edge_ordered[(d2p + d2p_delta) % N], o2) not in links
        else:
            # Unknown state
            raise NotImplementedError

        linked_pos = {p for p, _ in links}
        linked_idc = {i for i, p in enumerate(edge_ordered) if p in linked_pos}
        while True:
            d1p_pos = edge_ordered[d1p]
            d2p_pos = edge_ordered[d2p]
            # print("Consider", d1p_pos, d2p_pos, d1p, d2p)
            if o1 not in orientations[d1p] or o2 not in orientations[d2p]:
                # print("Change in orientation", orientations[d1p], o1, orientations[d2p], o2)
                break
            if (d1p_pos, o1) in links or (d2p_pos, o2) in links:
                # print("Already linked")
                break
            # print("LINK", d1p_pos, d2p_pos)
            links[(d1p_pos, o1)] = (d2p_pos, tuple(-x for x in o2))
            links[(d2p_pos, o2)] = (d1p_pos, tuple(-x for x in o1))
            d1p = (d1p + d1p_delta) % N
            d2p = (d2p + d2p_delta) % N
    # print(possible_link_locations)
    
    edge_with_orientation = {(p, o) for p, os in zip(edge_ordered, orientations) for o in os}
    assert len(edge_with_orientation - set(links)) == 0
        
    adjacency = defaultdict(dict)
    positions = {k for k, v in active_positions.items() if v == EMPTY}
    for pos in positions:
        # Up
        next_pos = (pos[0] - 1, pos[1])
        next_dir = (-1, 0)
        if next_pos not in active_positions:
            assert (pos, next_dir) in links
            next_pos, next_dir = links[(pos, next_dir)]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(-1, 0)] = (next_pos, next_dir)

        # Down
        next_pos = (pos[0] + 1, pos[1])
        next_dir = (1, 0)
        if next_pos not in active_positions:
            assert (pos, next_dir) in links
            next_pos, next_dir = links[(pos, next_dir)]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(1, 0)] = (next_pos, next_dir)

        # Right
        next_pos = (pos[0], pos[1] + 1)
        next_dir = (0, 1)
        if next_pos not in active_positions:
            assert (pos, next_dir) in links
            next_pos, next_dir = links[(pos, next_dir)]

        if active_positions[next_pos] == EMPTY:
            assert isinstance(next_dir, tuple) and len(next_dir) == 2
            adjacency[pos][(0, 1)] = (next_pos, next_dir)

        # Left
        next_pos = (pos[0], pos[1] - 1)
        next_dir = (0, -1)
        if next_pos not in active_positions:
            assert (pos, next_dir) in links
            next_pos, next_dir = links[(pos, next_dir)]

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
