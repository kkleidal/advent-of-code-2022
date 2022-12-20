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

@dataclass(frozen=True)
class State:
    resources: Tuple[int, int, int, int]
    robots: Tuple[int, int, int, int]
    pending_robots: Tuple[int, int, int, int]
    time: int = 0

    def prune_state(self):
        if any(self.pending_robots):
            return None
        return self.resources + self.robots

    def get_key(self, blueprint):
        # TODO: maybe Upperbound on potential geodes, obsideon, clay, ore if trying to maximize each
        ...

    def sufficient_resources(self, reqs):
        for k, v in reqs.items():
            if self.resources[k] < v:
                return False
        return True

    def missing_resources(self, reqs):
        missing = {}
        for k, v in reqs.items():
            if self.resources[k] < v:
                missing[k] = v - self.resources[k]
        return missing

    def start_making_bot(self, bot, reqs):
        assert self.sufficient_resources(reqs)
        return dataclasses.replace(self,
            resources=tuple(c - reqs.get(i, 0) for i, c in enumerate(self.resources)),
            pending_robots=tuple(c + (1 if i == bot else 0) for i, c in enumerate(self.pending_robots)),
        )

    def time_step(self):
        return dataclasses.replace(self,
            resources=tuple(c + self.robots[i] for i, c in enumerate(self.resources)),
            robots=tuple(c + self.pending_robots[i] for i, c in enumerate(self.robots)),
            pending_robots=tuple(0 for i, c in enumerate(self.pending_robots)),
            time=self.time + 1,
        )
        

best_found = None

def clear_print_state():
    global best_found, prune1, prune2
    best_found = 0
    prune1 = 0
    prune2 = 0

import time
def maybe_print(val):
    global best_found
    now = time.time()
    if best_found is None or val > best_found:
        best_found = val
        print("Best found:", best_found, prune1, prune2)
    

def will_waiting_let_me_build_a_bot_we_cant_build_now(state, blueprint):
    for bot, reqs in reversed(blueprint.items()):
        missing_resources = state.missing_resources(reqs)
        if all(state.robots[k] > 0 for k in missing_resources):
            # We'll get there eventually
            return True
    return False
    
def find_optimal_strategy_recurse(blueprint, state, cache, prune_cache, prune_cache2):
    global prune1, prune2
    if state.time == MAX_TIME:
        maybe_print(state.resources[ORDER.index("geode")])
        return state.resources[ORDER.index("geode")]
    if state not in cache:
        prune_state = state.prune_state()
        if prune_state:
            t = state.time
            if t not in prune_cache:
                prune_cache[t] = []
            if prune_cache[t] and any(all(e1 <= e2 for e1, e2 in zip(prune_state, pc)) for pc in prune_cache[t]):
                cache[state] = 0
                prune1 += 1
                # print("PRUNE")
                return cache[state]
            if prune_state in prune_cache2:
                if prune_cache2[prune_state] <= t:
                    cache[state] = 0
                    prune2 += 1
                    return cache[state]
    
        # print(state)
        def next_possib_states():
            can_build = False
            for bot, reqs in reversed(blueprint.items()):
                if state.sufficient_resources(reqs):
                    can_build = True
                    yield state.start_making_bot(bot, reqs)
            if not can_build or will_waiting_let_me_build_a_bot_we_cant_build_now(state, blueprint):
                # Otherwise, there's no point in waiting
                yield state.time_step()

        if prune_state:
            prune_cache[t].append(prune_state)
            if prune_state not in prune_cache2 or prune_cache2[prune_state] > t:
                prune_cache2[prune_state] = t

        best_outcome = max(find_optimal_strategy_recurse(blueprint, next_state, cache, prune_cache, prune_cache2)
                           for next_state in next_possib_states())
        # print(f"Cache for {state.time}")
        cache[state] = best_outcome
    return cache[state]
    
def find_optimal_strategy_geodes(blueprint):
    # pq = PriorityQueue()
    blueprint_ind = {ORDER.index(k): {ORDER.index(k2): v2 for k2, v2 in v.items()} for k, v in blueprint.items()}
    empty = (0, 0, 0, 0)
    state = State(resources=empty, robots=(0, 0, 0, 1), pending_robots=empty)
    return find_optimal_strategy_recurse(blueprint_ind, state, {}, {}, {})
        
def main():
    blueprints = parse()
    score = 0
    for index, blueprint in blueprints.items():
        clear_print_state()
        geodes = find_optimal_strategy_geodes(blueprint)
        score += index * geodes
    return score

if __name__ == "__main__":
    print(main())
