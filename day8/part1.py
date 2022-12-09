import sys

grid = []
for line in sys.stdin:
    line = line.strip()
    if line:
        grid.append(list(map(int, line)))

H = len(grid)
W = len(grid[0])

seen = set()
for y in range(H):
    for x in range(W):
        for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            cy, cx = y, x

            cur = grid[cy][cx]
            cy += dy
            cx += dx
            found = True
            while cy >= 0 and cy < H and cx >= 0 and cx < W:
                nxt = grid[cy][cx]
                if nxt >= cur:
                    found = False
                    break
                cy += dy
                cx += dx
            if found:
                seen.add((y, x))

# for y in range(H):
#     for x in range(W):
#         print("#" if (y, x) in seen else ".", end="")
#     print()
print(len(seen))
