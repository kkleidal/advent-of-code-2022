from part1 import *

def main(track_hist=False):
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

    def upper_bound_pressure(current_pressure, valves_on, my_room, elephant_room, time_remaining):
        potential = current_pressure
        rooms = [my_room, elephant_room]
        for valve_room, rate in room_to_valve_rate.items():
            if valve_room in valves_on:
                continue
            potential += max(0, time_remaining - min(shortest_paths[room][valve_room] for room in rooms) - 1) * rate
        return potential

    seen = {}
    pq.put((-upper_bound_pressure(0, set(), start_room, start_room, 26), 0, -26, start_room, start_room, set(), []))
    while not pq.empty():
        neg_potential_pressure, neg_pressure, neg_minutes_remaining, my_room, elephant_room, valves_on, hist = pq.get()
        potential_pressure = -neg_potential_pressure
        pressure = -neg_pressure
        minutes_remaining = -neg_minutes_remaining
        
        # Important: prune redundant states so we don't waste time going in cycles
        state = (my_room, elephant_room, frozenset(valves_on))
        if state in seen and seen[state] >= minutes_remaining:
            continue
        else:
            seen[state] = minutes_remaining

        print(potential_pressure, pressure)
        if potential_pressure == pressure:
            return pressure, hist

        my_next_states = []
        if my_room not in valves_on and room_to_valve_rate[my_room] > 0:
            # Option of turning valve on:
            new_minutes_remaining = minutes_remaining - 1
            add_pressure = new_minutes_remaining * room_to_valve_rate[my_room]
            new_room = my_room
            new_valves_on = set(valves_on) | {my_room}
            my_next_states.append((add_pressure, new_room, new_valves_on, ("OPEN", my_room)))
            # pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_room, new_valves_on, hist))

        # Neighbors with valves we could open
        priority_neighbors = sorted([n for n in adjacency_list[my_room] if n not in valves_on and room_to_valve_rate[n]], key=lambda n: -room_to_valve_rate[n])
        # Neighbors with 0 valves
        priority_neighbors2 = [n for n in adjacency_list[my_room] if n not in valves_on and n not in priority_neighbors]
        # Neighbors we've opened valves in
        neighbors = [n for n in adjacency_list[my_room] if n not in priority_neighbors and n not in priority_neighbors2]
        
        all_neighbors = priority_neighbors + priority_neighbors2 + neighbors
        for neighbor in all_neighbors:
            # Option of moving rooms:
            new_minutes_remaining = minutes_remaining - 1
            new_pressure = pressure
            new_room = neighbor
            new_valves_on = valves_on
            my_next_states.append((0, new_room, new_valves_on, ("MOVE", new_room)))
            # pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_room, new_valves_on, hist))

        # ELEPHANT
        for my_state in my_next_states:
            # Important to have this loop so elephant can't turn on valves that are already on
            valves_on = my_state[2]

            elephant_next_states = []
            if elephant_room not in valves_on and room_to_valve_rate[elephant_room] > 0:
                # Option of turning valve on:
                new_minutes_remaining = minutes_remaining - 1
                add_pressure = new_minutes_remaining * room_to_valve_rate[elephant_room]
                new_room = elephant_room
                new_valves_on = set(valves_on) | {elephant_room}
                elephant_next_states.append((add_pressure, new_room, new_valves_on, ("OPEN", elephant_room)))
                # pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_room, new_valves_on, hist))

            # Neighbors with valves we could open
            priority_neighbors = sorted([n for n in adjacency_list[elephant_room] if n not in valves_on and room_to_valve_rate[n]], key=lambda n: -room_to_valve_rate[n])
            # Neighbors with 0 valves
            priority_neighbors2 = [n for n in adjacency_list[elephant_room] if n not in valves_on and n not in priority_neighbors]
            # Neighbors we've opened valves in
            neighbors = [n for n in adjacency_list[elephant_room] if n not in priority_neighbors and n not in priority_neighbors2]
            
            all_neighbors = priority_neighbors + priority_neighbors2 + neighbors
            for neighbor in all_neighbors:
                # Option of moving rooms:
                new_minutes_remaining = minutes_remaining - 1
                new_pressure = pressure
                new_room = neighbor
                new_valves_on = valves_on
                elephant_next_states.append((0, new_room, new_valves_on, ("MOVE", new_room)))

            for elephant_state in elephant_next_states:
                new_pressure = pressure + my_state[0] + elephant_state[0]
                new_minutes_remaining = minutes_remaining - 1
                new_my_room = my_state[1]
                new_elephant_room = elephant_state[1]
                new_valves_on = my_state[2] | elephant_state[2]
                hist = (hist + [(my_state[3], elephant_state[3])]) if track_hist else []
                pq.put((-upper_bound_pressure(new_pressure, new_valves_on, new_my_room, new_elephant_room, new_minutes_remaining), -new_pressure, -new_minutes_remaining, new_my_room, new_elephant_room, new_valves_on, hist))
    assert False
                
        


if __name__ == "__main__":
    pressure, hist = main()
    for evt in hist:
        print(evt)
    print(pressure)
