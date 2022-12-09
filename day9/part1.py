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
head_pos = zero
tail_pos = head_pos
visited = {tail_pos}
for direction in directions:
    head_pos = vec_add(head_pos, direction)
    diff = vec_sub(head_pos, tail_pos)
    if any(abs(x) > 1 for x in diff):
        step = tuple(sgn(x) for x in diff)
        tail_pos = vec_add(tail_pos, step)
    visited.add(tail_pos)
print(len(visited))
