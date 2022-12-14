from part1 import *

def simulate(occupied):
    floor = max(y for x, y in occupied) + 2

    def is_occupied(x, y):
        return (x, y) in occupied or y == floor

    units_of_sand_at_rest = 0
    while True:
        # draw(occupied)
        sx, sy = 500, 0
        while True:
            if not is_occupied(sx, sy+1):
                sy += 1
            elif not is_occupied(sx-1, sy+1):
                sx -= 1
                sy += 1
            elif not is_occupied(sx+1, sy+1):
                sx += 1
                sy += 1
            else:
                # comes to rest
                break
        occupied[(sx, sy)] = SAND
        units_of_sand_at_rest += 1
        if (sx, sy) == (500, 0):
            break
    return units_of_sand_at_rest

if __name__ == "__main__":
    occupied = load_initial_state()
    print(simulate(occupied))
