from part1 import parse, rock_sprites, Rock

def main():
    rocks_stopped = 0
    world = {}
    directions = parse()
    # directions = list(">>><<<")
    # directions = ["<"]

    rock_sprites_i = 0
    directions_i = 0

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

    highest_surface = [-1 for _ in range(7)]

    state_to_height = {}
    state_history = []
    state_to_i = {}

    target = 1000000000000
    while rocks_stopped < target:
        relative_surface = [s - min(highest_surface) for s in highest_surface]
        state = (tuple(relative_surface), rock_sprites_i, directions_i)
        state_history.append(state)
        if state not in state_to_height:
            state_to_height[state] = highest_so_far
            state_to_i[state] = len(state_history) - 1
        else:
            cycle_height = highest_so_far - state_to_height[state]
            cycle_length = len(state_history) - state_to_i[state] - 1
            print(f"Found cycle at {rocks_stopped} of length {cycle_length} and height {cycle_height}")
            start_cycle = state_to_i[state]
            start_height = state_to_height[state]

            def get_pred(target):
                full_cycles = (target - start_cycle) // cycle_length
                rem = (target - start_cycle) % cycle_length
                rem_height = state_to_height[state_history[start_cycle + rem]] - state_to_height[state]
                final_height = full_cycles * cycle_height + rem_height + start_height
                return final_height
            return get_pred(target) + 1

        rock_sprite = rock_sprites[rock_sprites_i]
        rock_sprites_i = (rock_sprites_i + 1) % len(rock_sprites)

        rock = Rock(rock_sprite, 2, 4 + highest_so_far)
        while True:
            direction = directions[directions_i]
            directions_i = (directions_i + 1) % len(directions)

            if direction == "<":
                rock.move_left()
            else:
                rock.move_right()
            if rock.intersects_with(world):
                rock.undo()
            rock.move_down()
            int_type = rock.intersects_with(world)
            if int_type:
                rock.undo()
            if int_type == 2:
                for x, y in rock.locs():
                    world[(x, y)] = True
                    highest_so_far = max(highest_so_far, y)
                    highest_surface[x] = max(highest_surface[x], y)
                break
        rocks_stopped += 1
    return highest_so_far + 1


if __name__ == '__main__':
    print(main())
