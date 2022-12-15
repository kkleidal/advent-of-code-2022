import sys
from part1 import parse, mdist, get_segments_on_row
import tqdm
import multiprocessing
from functools import partial

def try_find_solution(y, sensor_loc_and_dist, beacon_locs):
    segs, _, count = get_segments_on_row(sensor_loc_and_dist, beacon_locs, y)
    if len(segs) > 1:
        assert len(segs) == 2
        return (segs[0][1] + 1) * 4000000 + y
    
def main():
    extremes = int(sys.argv[1])
    sensor_info = parse()

    sensor_loc_and_dist = [(sensor_loc, mdist(sensor_loc, beacon_loc)) for sensor_loc, beacon_loc in sensor_info]
    beacon_locs = set(beacon_loc for _, beacon_loc in sensor_info)

    # About 3 minutes without multiproc, 1 minute with multiproc.
    # Maybe could have found something more optimal algorithmically,
    # but optimizing in 1D and bruteforcing in the second dimension worked out.
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for res in tqdm.tqdm(pool.imap_unordered(partial(try_find_solution,
            sensor_loc_and_dist=sensor_loc_and_dist,
            beacon_locs=beacon_locs,
        ),
        range(0, extremes)), total=extremes):
            if res:
                return res
    assert False, "No solution found"

if __name__ == "__main__":
    print(main())
