from part1 import *

def main():
    state = State(parse())
    # state.print()
    i = 0
    while True:
        print(i)
        last_elves = state.elves
        state = state.round()
        new_elves = state.elves
        i += 1
        if new_elves == last_elves:
            break
    return i

if __name__ == "__main__":
    print(main())
