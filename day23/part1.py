import sys
from collections import defaultdict

def parse():
    elves = set()
    for i, line in enumerate(sys.stdin):
        if line := line.strip():
            for j, c in enumerate(line):
                if c == "#":
                    elves.add((i, j))
    return elves

INITIAL_DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

class State:
    def __init__(self, elves, directions=INITIAL_DIRECTIONS):
        self.elves = elves
        self.directions = directions

    def neighbors(self, pos, diag=True):
        i, j = pos
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == dj == 0:
                    continue
                if abs(di) == abs(dj) and not diag:
                    continue
                pos_n = i + di, j + dj
                yield pos_n

    def round(self):
        new_elves = set()
        elf_to_proposal = {}
        proposal_to_elves = defaultdict(set)
        for pos_elf in self.elves:
            # if pos_elf == (2, 0):
            #     print(set(self.neighbors(pos_elf)))
            #     blech
                
            occupied_neighbors = set(self.neighbors(pos_elf)) & self.elves
            found = False
            if len(occupied_neighbors) > 0:
                for direction in self.directions:
                    available = True
                    for i in range(-1, 2):
                        consider_delta = tuple(x if x != 0 else i for x in direction)
                        consider_pos = tuple(x + y for x, y in zip(pos_elf, consider_delta))
                        if consider_pos in self.elves:
                            available = False
                            break
                    if available:
                        proposal = tuple(x + y for x, y in zip(pos_elf, direction))
                        elf_to_proposal[pos_elf] = proposal
                        proposal_to_elves[proposal].add(pos_elf)
                        found = True
                        break
            if not found:
                new_elves.add(pos_elf)
        for elf, proposal in elf_to_proposal.items():
            if proposal_to_elves[proposal] == {elf}:
                new_elves.add(proposal)
            else:
                new_elves.add(elf)
        assert len(new_elves) == len(self.elves)
        return State(new_elves, self.directions[1:] + self.directions[:1])

    def bbox(self):
        min_y = min(y for x, y in self.elves)
        max_y = max(y for x, y in self.elves)
        min_x = min(x for x, y in self.elves)
        max_x = max(x for x, y in self.elves)
        return (min_y, max_y + 1), (min_x, max_x + 1)

    def score(self):
        y_rng, x_rng = self.bbox()
        return (y_rng[1] - y_rng[0]) * (x_rng[1] - x_rng[0]) - len(self.elves)
    
    def print(self):
        y_rng, x_rng = self.bbox()
        for i in range(*y_rng):
            for j in range(*x_rng):
                print("#" if (i, j) in self.elves else ".", end="")
            print()
        print()

def main():
    state = State(parse())
    # state.print()
    for _ in range(10):
        state = state.round()
        # state.print()
    return state.score()

if __name__ == "__main__":
    print(main())
