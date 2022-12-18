import sys

def parse():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield tuple(map(int, line.split(",")))

def directions():
    for coord in range(3):
        for direction in [-1, 1]:
            yield tuple(direction if i == coord else 0 for i in range(3))
def main():
    nodes = set(parse())
    faces = 0
    for x, y, z in nodes:
        for dx, dy, dz in directions():
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in nodes:
                faces += 1
    return faces

if __name__ == "__main__":
    print(main())
