import sys

def load_lines():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield line

def parse():
    for line in load_lines():
        yield [tuple(map(int, coord_pair.split(","))) for coord_pair in line.split(" -> ")]

def sgn(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

def draw(occupied):
    ys = min(0, min(y for x, y in occupied)) - 0
    xs = min(500, min(x for x, y in occupied)) - 1
    ye = max(0, max(y for x, y in occupied)) + 1
    xe = max(500, max(x for x, y in occupied)) + 1
    for y in range(ys, ye+1):
        for x in range(xs, xe+1):
            if y == 0 and x == 500:
                assert (x, y) not in occupied
                print("+", end="")
            else:
                print(chars[occupied.get((x, y), 0)], end="")
        print()
    print()

ROCK = 1
SAND = 2

chars = {
    0: ".",
    ROCK: "#",
    SAND: "o",
}

def load_initial_state():
    occupied = {}
    for line in parse():
        x, y = line[0]
        occupied[(x, y)] = ROCK
        for end_x, end_y in line[1:]:
            if end_x != x:
                dx = sgn(end_x - x)
                dy = 0
            else:
                assert end_y != y
                dx = 0
                dy = sgn(end_y - y)
            while not (x == end_x and y == end_y):
                x += dx
                y += dy
                occupied[(x, y)] = ROCK
    return occupied


def simulate(occupied):
    floor = max(y for x, y in occupied) + 1
    units_of_sand_at_rest = 0
    while True:
        # draw(occupied)
        sx, sy = 500, 0
        at_rest = False
        while sy <= floor:
            if (sx, sy+1) not in occupied:
                sy += 1
            elif (sx-1, sy+1) not in occupied:
                sx -= 1
                sy += 1
            elif (sx+1, sy+1) not in occupied:
                sx += 1
                sy += 1
            else:
                # comes to rest
                at_rest = True
                break
        if not at_rest:
            break
        occupied[(sx, sy)] = SAND
        units_of_sand_at_rest += 1
    return units_of_sand_at_rest

if __name__ == "__main__":
    occupied = load_initial_state()
    print(simulate(occupied))
