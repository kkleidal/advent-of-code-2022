import sys
from typing import Tuple, Any
from dataclasses import dataclass
from collections import defaultdict
import dataclasses
from queue import PriorityQueue
from frozendict import frozendict

@dataclass(frozen=True)
class Blizzard:
    position: Tuple[int, int]
    direction: Tuple[int, int]

def parse():
    valid_squares = set()
    blizzards = defaultdict(set)
    start = None
    end = None
    for i, line in enumerate(sys.stdin):
        if line := line.strip():
            for j, c in enumerate(line):
                if c in (".", ">", "<", "^", "v"):
                    valid_squares.add((i, j))
                    end = (i, j)
                    if start is None:
                        start = (i, j)
                    if c == ">":        
                        blizzards[(i, j)].add(Blizzard((i, j), (0, 1)))
                    elif c == "v":        
                        blizzards[(i, j)].add(Blizzard((i, j), (1, 0)))
                    elif c == "<":        
                        blizzards[(i, j)].add(Blizzard((i, j), (0, -1)))
                    elif c == "^":        
                        blizzards[(i, j)].add(Blizzard((i, j), (-1, 0)))
    return blizzards, valid_squares, start, end

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def build_blizzard_adjacency_map(valid_squares):
    adj = defaultdict(dict)
    for i, j in valid_squares:
        pos = (i, j)
        for di, dj in DIRECTIONS:
            d = (di, dj)
            neighbor = (i + di, j + dj)
            if neighbor not in valid_squares:
                change_ind = 1 if di == 0 else 0
                fix_ind = 1 - change_ind
                agg = max if d[change_ind] < 0 else min
                _, neighbor = agg((p[change_ind], p) for p in valid_squares if p[fix_ind] == pos[fix_ind])
                assert neighbor in valid_squares
            adj[pos][d] = neighbor
    return adj

def build_self_adjacency_map(valid_squares):
    adj = defaultdict(dict)
    for i, j in valid_squares:
        adj[i, j][(0, 0)] = (i, j)
        pos = (i, j)
        for di, dj in DIRECTIONS:
            d = (di, dj)
            neighbor = (i + di, j + dj)
            if neighbor not in valid_squares:
                continue
            adj[pos][d] = neighbor
    return adj
                    
# Ironic:
def freeze_blizzards(blizzards):
    return frozendict({k: frozenset(v) for k, v in blizzards.items()})

def progress_blizzard_state(blizzards, badj):
    new_blizzards = defaultdict(set)
    for pos, blizz_at_pos in blizzards.items():
        for blizz in blizz_at_pos:
            new_blizz = dataclasses.replace(blizz, position=badj[pos][blizz.direction])
            new_blizzards[new_blizz.position].add(new_blizz)
    return freeze_blizzards(new_blizzards)

# def render(valid_squares, blizzards):
#     min_y = min(y for y, x in valid_squares)
#     max_y = max(y for y, x in valid_squares)
#     min_x = min(x for y, x in valid_squares)
#     max_x = max(x for y, x in valid_squares)
#     for i in range(min_y - 1, max_y + 2):
#         for j in range(min_x - 1, max_x + 2):
#             if (i, j) in valid_squares:
#                 bat = blizzards[(i, j)]
#                 if len(bat) == 0:
#                     c = "."
#                 elif len(bat) == 1:
#                     c = {
#                         (0, 1): ">",
#                         (1, 0): "v",
#                         (0, -1): "<",
#                         (-1, 0): "^",
#                     }[min(bat).direction]
#                 elif len(bat) > 1 and len(bat) < 10:
#                     c = str(len(bat))
#                 else:
#                     c = "+"
#             else:
#                 c = "#"
#             print(c, end="")
#         print()
#     print()

def render(s):
    min_y = min(y for y, x in s.valid_squares)
    max_y = max(y for y, x in s.valid_squares)
    min_x = min(x for y, x in s.valid_squares)
    max_x = max(x for y, x in s.valid_squares)
    for i in range(min_y - 1, max_y + 2):
        for j in range(min_x - 1, max_x + 2):
            if (i, j) in s.valid_squares:
                bat = s.blizzards.get((i, j), set())
                if (i, j) == s.position:
                    c = "E" 
                elif len(bat) == 0:
                    c = "."
                elif len(bat) == 1:
                    c = {
                        (0, 1): ">",
                        (1, 0): "v",
                        (0, -1): "<",
                        (-1, 0): "^",
                    }[min(bat).direction]
                elif len(bat) > 1 and len(bat) < 10:
                    c = str(len(bat))
                else:
                    c = "+"
            else:
                c = "#"
            print(c, end="")
        print()
    print()


@dataclass(frozen=True)
class State:
    time: int
    position: Tuple[int, int]
    blizzards: Any
    valid_squares: Any
    end: Tuple[int, int]

    def __gt__(self, other):
        return self.time > other.time or self.position > other.position

    def key(self):
        heuristic = sum(abs(x - y) for x, y in zip(self.position, self.end))
        return self.time + heuristic

    def visited_key(self):
        return (self.blizzards, self.position)

    def is_dead(self):
        return len(self.blizzards.get(self.position, set())) > 0

    def is_terminal(self):
        return self.position == self.end and not self.is_dead()
        

def main():
    blizzards, valid_squares, start, end = parse()
    badj = build_blizzard_adjacency_map(valid_squares)
    padj = build_self_adjacency_map(valid_squares)
    # render(valid_squares, blizzards)
    # for _ in range(18):
    #     blizzards = progress_blizzard_state(blizzards, badj)
    # render(valid_squares, blizzards)
    best_logged = None
    def maybe_log(s):
        nonlocal best_logged
        v = sum(abs(x - y) for x, y in zip(s.position, s.end))
        if best_logged is None or best_logged > v:
            best_logged = v
            print(f"Closest found: {v}")

    blizz_cache = {}
    def next_blizzards(s):
        if s.time not in blizz_cache:
            new_blizzards = progress_blizzard_state(s.blizzards, badj)
            blizz_cache[s.time] = new_blizzards
        return blizz_cache[s.time]
        
    
    s = State(0, start, freeze_blizzards(blizzards), frozenset(valid_squares), end)
    q = PriorityQueue()
    q.put((s.key(), s))
    visited = {s.visited_key()}
    while not q.empty():
        _, s = q.get()
        # render(s)
        if s.is_terminal():
            return s.time
        new_blizzards = next_blizzards(s)
        for d in DIRECTIONS + [(0, 0)]:
            if d in padj[s.position]:
                # print(f"Consider {d}")
                new_pos = padj[s.position][d]
                new_state = dataclasses.replace(s, position=new_pos, blizzards=new_blizzards, time=s.time + 1)
                vk = new_state.visited_key()
                if new_state.is_dead() or vk in visited:
                    # print("skip")
                    continue
                visited.add(vk)
                maybe_log(new_state)
                q.put((new_state.key(), new_state))
    assert False

if __name__ == "__main__":
    print(main())
