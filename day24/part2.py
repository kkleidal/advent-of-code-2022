from part1 import *

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

    
    def search(start, blizzards, end):
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
                return s.time, s.blizzards
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

    print("Phase 1")
    time1, blizzards = search(start, blizzards, end)
    print("Phase 2")
    time2, blizzards = search(end, blizzards, start)
    print("Phase 3")
    time3, blizzards = search(start, blizzards, end)
    return time1 + time2 + time3
    

if __name__ == "__main__":
    print(main())
