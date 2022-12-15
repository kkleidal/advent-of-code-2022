import sys
import re
import tqdm

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

def main():
    eval_at_row = int(sys.argv[1])
    sensor_info = parse()
    sensor_loc_and_dist = [(sensor_loc, mdist(sensor_loc, beacon_loc)) for sensor_loc, beacon_loc in sensor_info]
    x_start = min(min(sensor_loc[0], beacon_loc[0]) for sensor_loc, beacon_loc in sensor_info)
    x_end = max(max(sensor_loc[0], beacon_loc[0]) for sensor_loc, beacon_loc in sensor_info)

    beacon_locs = set(beacon_loc for _, beacon_loc in sensor_info)
    
    def is_in_range(pt):
        return any(mdist(sloc, pt) <= nearest for sloc, nearest in sensor_loc_and_dist)

    def counts_as_cannot_be_present(pt):
        return is_in_range(pt) and pt not in beacon_locs

    # Could be more efficient by identifing where cone intersects with y and assuming
    # all points on line seg are covered, except beacons on the line seg, but that's more
    # complicated. We'd also have to combine intersecting line segments
    y = eval_at_row
    print("Sweeping left")
    while is_in_range((x_start, y)):
        x_start -= 1
    print("Sweeping right")
    while is_in_range((x_end, y)):
        x_end += 1

    total = 0
    print("Full sweep")
    for x in tqdm.trange(x_start, x_end):
        if counts_as_cannot_be_present((x, y)):
            total += 1

    return total

if __name__ == "__main__":
    print(main())
