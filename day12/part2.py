import networkx as nx
from part1 import parse, make_graph, height_of

def find_all_shortest_paths(grid, end, g):
    H = len(grid)
    W = len(grid[0])
    for i in range(H):
        for j in range(W):
            if grid[i][j] == height_of('a'):
                try:
                    path = nx.algorithms.shortest_path(g, (i, j), end, weight="weight")
                except nx.exception.NetworkXNoPath:
                    continue
                yield nx.path_weight(g, path, "weight"), path

if __name__ == '__main__':
    grid, _, end = parse()
    g = make_graph(grid)
    candidates = list(find_all_shortest_paths(grid, end, g))
    min_dist, _ = min(candidates)
    for dist, path in candidates:
        if dist == min_dist:
            print(len(path) - 1)
