import sys

grid = []
for line in sys.stdin:
    line = line.strip()
    if line:
        grid.append(list(map(int, line)))

H = len(grid)
W = len(grid[0])

seen = set()
scenic_scores_grid = []
for y in range(H):
    scenic_scores_row = []
    for x in range(W):
        scenic_score = 1
        for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            cy, cx = y, x

            cur = grid[cy][cx]
            cy += dy
            cx += dx
            found = True
            score = 0
            while cy >= 0 and cy < H and cx >= 0 and cx < W:
                score += 1
                nxt = grid[cy][cx]
                if nxt >= cur:
                    found = False
                    break
                cy += dy
                cx += dx
            if found:
                seen.add((y, x))
            scenic_score *= score
        scenic_scores_row.append(scenic_score)
    scenic_scores_grid.append(scenic_scores_row)
        

# for row in scenic_scores_grid:
#     print(row)
print(max(max(row) for row in scenic_scores_grid))
