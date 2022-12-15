import sys
import re
import heapq

def parse():
    pattern = re.compile(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")
    parsed = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            m = pattern.match(line)
            assert m
            xs, ys, xb, yb = map(int, m.groups())
            parsed.append(((xs, ys), (xb, yb)))
    return parsed
            
def mdist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def intersect_seg(seg, y):
    miny = min(pt[1] for pt in seg)
    maxy = max(pt[1] for pt in seg)
    if miny <= y and y <= maxy:
        slope_num = (seg[1][0] - seg[0][0])
        slope_den = (seg[1][1] - seg[0][1])
        assert abs(slope_num) == abs(slope_den)
        slope_x_div_y = slope_num // slope_den
        assert abs(slope_x_div_y) == 1
        intersect_x = seg[0][0] + slope_x_div_y * (y - seg[0][1])
        return intersect_x
    else:
        return None

def find_intersections(sensor_loc, dist, y):
    xs, ys = sensor_loc

    east = (xs + dist, ys)
    west = (xs - dist, ys)
    north = (xs, ys - dist)
    south = (xs, ys + dist)

    north_west = (north, west)
    north_east = (north, east)
    south_east = (south, east)
    south_west = (south, west)

    north_cone = (north_west, north_east)
    south_cone = (south_west, south_east)

    intersections = []
    for cone in [north_cone, south_cone]:
        pts = tuple((intersect_seg(seg, y) for seg in cone))
        if all(pt is not None for pt in pts):
            intersections.append(pts)
    if intersections:
        return intersections[0]
    else:
        return None
    
            

def get_segments_on_row(sensor_loc_and_dist, beacon_locs, y):
    intersections = []
    for sensor_loc, dist in sensor_loc_and_dist:
        intersect = find_intersections(sensor_loc, dist, y)
        if intersect is not None:
            intersections.append(intersect)

    START = 0
    BEACON = 1
    END = 2

    event_queue = []
    for start, end in intersections:
        event_queue.append((start, START, end))
    for xb, yb in beacon_locs:
        if yb == y:
            event_queue.append((xb, BEACON))
    heapq.heapify(event_queue)

    inside_count = 0
    inside_start = 0
    beacons_inside = 0

    seg_counts = []
    segs = []
    while event_queue:
        evt = heapq.heappop(event_queue)
        if evt[1] == START:
            if inside_count == 0:
                inside_start = evt[0]
                beacons_inside = 0
            inside_count += 1
            heapq.heappush(event_queue, (evt[2], END))
        elif evt[1] == BEACON:
            assert inside_count > 0
            beacons_inside += 1
        else:
            assert evt[1] == END
            inside_count -= 1
            if inside_count == 0:
                segs.append((inside_start, evt[0], beacons_inside))
                seg_counts.append(1 + evt[0] - inside_start - beacons_inside)
                inside_start = 0
                beacons_inside = 0
    
    return segs, seg_counts, sum(seg_counts)
            

def main():
    eval_at_row = int(sys.argv[1])
    sensor_info = parse()


    # Identifing where cone intersects with y and assuming
    # all points on line seg are covered, except beacons on the line seg.
    # Then combine segments using a priority queue (heap)
    sensor_loc_and_dist = [(sensor_loc, mdist(sensor_loc, beacon_loc)) for sensor_loc, beacon_loc in sensor_info]
    beacon_locs = set(beacon_loc for _, beacon_loc in sensor_info)
    _, _, count = get_segments_on_row(sensor_loc_and_dist, beacon_locs, eval_at_row)
    return count

if __name__ == "__main__":
    print(main())
