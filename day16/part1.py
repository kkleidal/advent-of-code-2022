import sys
import re
from queue import PriorityQueue
import networkx as nx

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

def parse():
    pat = re.compile("^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)$")
    for line in sys.stdin:
        line = line.strip()
        if line:
            m = pat.match(line)
            assert m
            cur_room = m.group(1)
            valve_rate = int(m.group(2))
            neighbor_rooms = m.group(3).split(", ")
            yield cur_room, valve_rate, neighbor_rooms

def main():
    start_room = 'AA'
    rooms = set()
    adjacency_list = {}
    room_to_valve_rate = {}
    for cur_room, valve_rate, neighbor_rooms in parse():
        rooms.add(cur_room)
        rooms.update(neighbor_rooms)
        adjacency_list[cur_room] = neighbor_rooms
        room_to_valve_rate[cur_room] = valve_rate

    pq = PriorityQueue()
    
    g = nx.Graph()    
    for room in rooms:
        g.add_node(room)
    for room, neighbors in adjacency_list.items():
        for n in neighbors:
            g.add_edge(room, n)
    shortest_paths = dict(nx.algorithms.all_pairs_shortest_path_length(g))
    print(shortest_paths)

    def upper_bound_pressure(current_pressure, valves_on, room, time_remaining):
        potential = current_pressure
        for valve_room, rate in room_to_valve_rate.items():
            if valve_room in valves_on:
                continue
            potential += max(0, time_remaining - shortest_paths[room][valve_room] - 1) * rate
        return potential

    seen = {}
    pq.put((-upper_bound_pressure(0, set(), start_room, 30), 0, -30, start_room, set(), []))
    while not pq.empty():
        neg_potential_pressure, neg_pressure, neg_minutes_remaining, room, valves_on, hist = pq.get()
        potential_pressure = -neg_potential_pressure
        pressure = -neg_pressure
        minutes_remaining = -neg_minutes_remaining
        
        # Important: prune redundant states so we don't waste time going in cycles
        state = (room, frozenset(valves_on))
        if state in seen and seen[state] >= minutes_remaining:
            continue
        else:
            seen[state] = minutes_remaining

        print(potential_pressure, pressure)
        if potential_pressure == pressure:
            return pressure, hist
        if room not in valves_on and room_to_valve_rate[room] > 0:
            # Option of turning valve on:
            new_minutes_remaining = minutes_remaining - 1
            add_pressure = new_minutes_remaining * room_to_valve_rate[room]
            hist = [] # list(hist) + [("OPEN", room, add_pressure)]
            new_pressure = pressure + add_pressure
            new_room = room
            new_valves_on = set(valves_on) | {room}
            pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_room, new_valves_on, hist))

        # Neighbors with valves we could open
        priority_neighbors = sorted([n for n in adjacency_list[room] if n not in valves_on and room_to_valve_rate[n]], key=lambda n: -room_to_valve_rate[n])
        # Neighbors with 0 valves
        priority_neighbors2 = [n for n in adjacency_list[room] if n not in valves_on and n not in priority_neighbors]
        # Neighbors we've opened valves in
        neighbors = [n for n in adjacency_list[room] if n not in priority_neighbors and n not in priority_neighbors2]
        
        all_neighbors = priority_neighbors + priority_neighbors2 + neighbors
        for neighbor in all_neighbors:
            # Option of moving rooms:
            new_minutes_remaining = minutes_remaining - 1
            new_pressure = pressure
            new_room = neighbor
            new_valves_on = valves_on
            hist = [] # list(hist) + [("MOVE", neighbor)]
            pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_room, new_valves_on, hist))
        


if __name__ == "__main__":
    pressure, hist = main()
    for evt in hist:
        print(evt)
    print(pressure)
