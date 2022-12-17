import sys
import itertools

def parse():
    return list(sys.stdin.read().strip())

# rocks_def = """
# #####
# ....#
# 
# #....
# #####
# """

rocks_def = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

rock_sprites = []
for rock_def in rocks_def.strip().split("\n\n"):
    sprite = []
    for line in rock_def.split("\n"):
        row = [c == "#" for c in line]
        sprite.append(row)
    rock_sprites.append(sprite)

class Rock:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self._undo = []

    def move_left(self):
        self.x -= 1
        self._undo.append(self.move_right)

    def move_right(self):
        self.x += 1
        self._undo.append(self.move_left)

    def move_down(self):
        self.y -= 1
        self._undo.append(self.move_up)

    def move_up(self):
        self.y += 1
        self._undo.append(self.move_down)

    def undo(self):
        if len(self._undo) == 0:
            raise ValueError("Nothing to undo")
        self._undo.pop()()

    def locs(self):
        for j, row in enumerate(self.sprite):
            ry = len(self.sprite) - j - 1
            y = ry + self.y
            for rx, col in enumerate(row):
                x = rx + self.x
                if col:
                    yield x, y

    def has(self, x, y):
        return any((x, y) == loc for loc in self.locs())

    def intersects_with(self, world):
        for x, y in self.locs():
            if y < 0 or world.get((x, y)):
                return 2 
            elif x < 0 or x >= 7:
                return 1
        return 0

    def highest(self):
        return max(y for _, y in self.locs())

def main():
    rocks_stopped = 0
    world = {}
    directions = parse()
    rock_sprites_iter = iter(itertools.cycle(rock_sprites))
    directions_iter = iter(itertools.cycle(directions))
    highest_so_far = -1

    rock = None
    def render():
        top = highest_so_far
        if rock:
            top = max(top, rock.highest())
        for y in reversed(range(-1, top + 1)):
            for x in range(-1, 8):
                if y < 0:
                    print("-", end="")
                elif x < 0 or x >= 7:
                    print("|", end="")
                elif (x, y) in world:
                    print("#", end="")
                elif rock and rock.has(x, y):
                    print("@", end="")
                else:
                    print(".", end="")
            print()
        print()

    while rocks_stopped < 2022:
        # print()
        rock_sprite = next(rock_sprites_iter)
        rock = Rock(rock_sprite, 2, 4 + highest_so_far)
        while True:
            # render()
            # print(rock.x, rock.y)
            # time.sleep(0.5)
            if next(directions_iter) == "<":
                # print("Left")
                rock.move_left()
            else:
                # print("Right")
                rock.move_right()
            if rock.intersects_with(world):
                # print("Bounce")
                rock.undo()
            # print("Move down")
            rock.move_down()
            int_type = rock.intersects_with(world)
            if int_type:
                # print("Bounce")
                rock.undo()
            if int_type == 2:
                # print("Rest")
                for x, y in rock.locs():
                    world[(x, y)] = True
                    highest_so_far = max(highest_so_far, y)
                break
        rocks_stopped += 1
    # render()
    return highest_so_far + 1


if __name__ == '__main__':
    print(main())
