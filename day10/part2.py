from part1 import load_ops, execute


if __name__ == '__main__':
    screen = [[False for _ in range(40)] for _ in range(6)]
    output = 0
    for i, register in enumerate(execute(load_ops())):
        pos = i % (40 * 6)
        y = pos // 40
        x = pos % 40
        if abs(x - register) <= 1:
            screen[y][x] = True
    for row in screen:
        for col in row:
            print("█" if col else " ", end="")
        print()
