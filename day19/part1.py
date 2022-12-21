import sys
import re
from queue import PriorityQueue
import dataclasses
from dataclasses import dataclass
from typing import Dict, Tuple

def parse():
    unparsed = sys.stdin.read()
    p1 = re.compile(r"Blueprint (\d+):")
    p2 = re.compile(r"Each \b(\w+)\b robot costs (\d+ \w+(?: and \d+ \w+)?).")

    state = 0
    blueprints = {}
    while True:
        if state == 0:
            m = p1.search(unparsed)
            if not m:
                break
            index = int(m.group(1))
            robot_resources = {}
            state += 1
        elif state >= 1 and state <= 4:
            m = p2.search(unparsed)
            assert m, repr(unparsed)
            robot_type = m.group(1)
            resources = {resource: int(c) for c, resource in (g.split(" ") for g in m.group(2).split(" and "))}
            robot_resources[robot_type] = resources
            state = (state + 1) % 5
            if state == 0:
                blueprints[index] = robot_resources
        unparsed = unparsed[m.span()[1]:]
    return blueprints


MAX_TIME = 24

ORDER = ["geode", "obsidian", "clay", "ore"]

def ceil_div(x, y):
    if x == 0:
        return 0
    return x // y + (1 if x % y > 0 else 0)

@dataclass(frozen=True)
class State:
    time: int
    resources: Tuple[int, int, int, int]
    robots: Tuple[int, int, int, int]
    pending_robots: Tuple[int, int, int, int]
    
    def subsumes(self, other):
        # # WARNING: Possibly inadmissable heuristic:
        # if self.time <= other.time and self.resources[0] > other.resources[0] and self.robots[0] > other.robots[0]:
        #     return True
        # if self.time <= other.time and all(self.resources[i] >= other.resources[i] and self.robots[i] >= other.robots[i] for i in range(1)) and self.resources[1] > other.resources[1] and self.robots[1] > other.robots[1]:
        #     return True
        # # if self.time <= other.time and all(self.resources[i] >= other.resources[i] and self.robots[i] >= other.robots[i] for i in range(2)) and self.resources[2] > other.resources[2] and self.robots[2] > other.robots[2]:
        # #     return True
            
        return (
            self.time <= other.time
            and all(s >= o for s, o in zip(self.resources, other.resources))
            and all(s >= o for s, o in zip(self.robots, other.robots))
            and all(s >= o for s, o in zip(self.pending_robots, other.pending_robots))
        )

    def reachable_bots(self, blueprint):
        for bot, reqs in enumerate(blueprint):
            if all(req == 0 or rob > 0 or pending > 0 for rob, req, pending in zip(self.robots, reqs, self.pending_robots)):
                all_times = []
                for cur, rob, req, pending in zip(self.resources, self.robots, reqs, self.pending_robots):
                    time = 0
                    while cur < req:
                        time += 1
                        cur += rob
                        rob += pending
                        pending = 0
                    all_times.append(time)
                time = max(all_times)
                yield bot, time

    def build_bot(self, bot, blueprint):
        assert all(r >= blueprint[bot][i] for i, r in enumerate(self.resources))
        return dataclasses.replace(self,
            resources=tuple(r - blueprint[bot][i] for i, r in enumerate(self.resources)),
            pending_robots=tuple(p + (1 if i == bot else 0) for i, p in enumerate(self.pending_robots)),
        )

    def step(self):
        return dataclasses.replace(self,
            time=self.time+1,
            resources=tuple(r + bots for r, bots in zip(self.resources, self.robots)),
            robots=tuple(r + bots for r, bots in zip(self.robots, self.pending_robots)),
            pending_robots=tuple(0 for _ in self.pending_robots),
        )
        

def find_optimal_strategy_recurse(state, blueprint, cache, prune_cache):
    if state in cache:
        return cache[state]
    if state.time not in prune_cache:
        prune_cache[state.time] = []
    if any(cached.subsumes(state) for cached in prune_cache[state.time]):
        return 0
    # print(state)
    new_states = []
    for bot, time in state.reachable_bots(blueprint):
        new_state = state
        for _ in range(time):
            new_state = new_state.step()
        if new_state.time < MAX_TIME:
            new_state = new_state.build_bot(bot, blueprint)
            new_states.append(new_state)
    if len(new_states) == 0:
        new_state = state
        while new_state.time < MAX_TIME:
            new_state = new_state.step()
        cache[state] = new_state.resources[0]
    else:
        cache[state] = max(
            find_optimal_strategy_recurse(ns, blueprint, cache, prune_cache)
            for ns in new_states
        )
    prune_cache[state.time] = [cached for cached in prune_cache[state.time] if not state.subsumes(cached)] + [state]
    return cache[state]

def find_optimal_strategy_geodes(blueprint): 
    blueprint = [[blueprint[ORDER[i]].get(ORDER[j], 0) for j in range(4)] for i in range(4)]
    state = State(time=0, resources=(0, 0, 0, 0), robots=(0, 0, 0, 1), pending_robots=(0, 0, 0, 0))
    return find_optimal_strategy_recurse(state, blueprint, {}, {})

def main():
    blueprints = parse()
    score = 0
    for index, blueprint in blueprints.items():
        geodes = find_optimal_strategy_geodes(blueprint)
        print("-->", index, geodes)
        # for evt in hist:
        #     print("  ", evt)
        score += index * geodes
    return score

if __name__ == "__main__":
    print(main())
