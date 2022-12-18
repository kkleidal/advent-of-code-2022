from part1 import *
from collections import defaultdict
import networkx as nx

def full(tup, ind, val):
    return tuple(val if i == ind else o_val for i, o_val in enumerate(tup))

def main():
    nodes = set(parse())
    total_surf_area = 0
    air_blocks = defaultdict(int)
    for x, y, z in nodes:
        for dx, dy, dz in directions():
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in nodes:
                total_surf_area += 1
                air_blocks[neighbor] += 1

    def adjacent_to_cube(neighbor):
        x, y, z = neighbor
        for dx in range(-1, 0, 1):
            for dy in range(-1, 0, 1):
                for dz in range(-1, 0, 1):
                    if (x + dx, y + dy, z + dz) in nodes:
                        return True
        return False

    
    air_blocks = dict(air_blocks)
    for _ in range(3):
        new_airblocks = set()
        for cube in air_blocks:
            x, y, z = cube
            for dx, dy, dz in directions():
                neighbor = (x + dx, y + dy, z + dz)
                if neighbor not in nodes and neighbor not in air_blocks:
                    new_airblocks.add(neighbor)
        if new_airblocks:
            for airblock in new_airblocks:
                air_blocks[airblock] = 0
        else:
            break

    g = nx.Graph()
    for air_block in air_blocks:
        g.add_node(air_block)
    for air_block in air_blocks:
        x, y, z = air_block
        for dx, dy, dz in directions():
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in air_blocks:
                g.add_edge(air_block, neighbor)
    ccs = list(nx.algorithms.connected_components(g))

    max_bounds = tuple(max(n[i] for n in nodes) + 1 for i in range(3))
    min_bounds = tuple(min(n[i] for n in nodes) - 1 for i in range(3))

    def get_exterior_node():
        for i, cc in enumerate(ccs):
            for node in cc:
                x, y, z = node
                any_non_hits = False
                for dx, dy, dz in directions():
                    hits = False
                    while (x >= min_bounds[0] and x <= max_bounds[0] and y >= min_bounds[1] and y <= max_bounds[1]
                           and z >= min_bounds[2] and z <= max_bounds[2]):
                        x += dx
                        y += dy
                        z += dz
                        if (x, y, z) in nodes:
                            hits = True
                            break
                    if not hits:
                        return i, node

    surface_cc_index, start_node = get_exterior_node()

    surface_nodes = ccs[surface_cc_index]
    return sum(v for k, v in air_blocks.items() if k in surface_nodes)


if __name__ == "__main__":
    print(main())
