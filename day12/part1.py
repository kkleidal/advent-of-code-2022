import sys
import networkx as nx

def get_lines():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield line

def height_of(c):
    return ord(c) - ord('a')

def parse():
    start = None
    end = None
    rows = []
    for i, line in enumerate(get_lines()):
        row = []
        for j, c in enumerate(line):
            if c == "S":
                start = (i, j)
                row.append(height_of('a'))
            elif c == "E":
                end = (i, j)
                row.append(height_of('z'))
            else:
                row.append(height_of(c))
        rows.append(row)
    return rows, start, end

def make_graph(grid):
    g = nx.DiGraph()
    H = len(grid)
    W = len(grid[0])
    for i in range(H):
        for j in range(W):
            g.add_node((i, j), height=grid[i][j])
    for i in range(H):
        for j in range(W):
            cur_height = grid[i][j]
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + dy, j + dx
                if ni >= 0 and ni < H and nj >= 0 and nj < W:
                    nxt_height = grid[ni][nj]
                    if nxt_height - cur_height <= 1:
                        dist = abs(nxt_height - cur_height) + 1
                        g.add_edge((i, j), (ni, nj), weight=dist)
    return g

if __name__ == '__main__':
    grid, start, end = parse()
    g = make_graph(grid)
    path = nx.algorithms.shortest_path(g, start, end, weight="weight")
    print(len(path) - 1)
