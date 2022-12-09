import sys

direction_to_vec = {
    "U": (1, 0),
    "R": (0, 1),
    "D": (-1, 0),
    "L": (0, -1),
}

def vec_scalar_multiply(vec, s):
    return tuple(x * s for x in vec)

def vec_add(vec1, vec2):
    return tuple(x + y for x, y in zip(vec1, vec2))

def vec_sub(vec1, vec2):
    return tuple(x - y for x, y in zip(vec1, vec2))

def sgn(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

directions = []
for line in sys.stdin:
    line = line.strip()
    if line:
        direction, steps = line.split(" ")
        vec = direction_to_vec[direction]
        for _ in range(int(steps)):
            directions.append(vec)

zero = (0, 0)
knot_positions = [zero for _ in range(10)]
visited = {zero}
for direction in directions:
    knot_positions[0] = vec_add(knot_positions[0], direction)
    for i in range(1, len(knot_positions)):
        diff = vec_sub(knot_positions[i-1], knot_positions[i])
        if any(abs(x) > 1 for x in diff):
            step = tuple(sgn(x) for x in diff)
            knot_positions[i] = vec_add(knot_positions[i], step)
    visited.add(knot_positions[-1])
print(len(visited))
