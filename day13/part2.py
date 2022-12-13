from part1 import parse, compare
import itertools
from functools import cmp_to_key

if __name__ == "__main__":
    packets = itertools.chain.from_iterable(parse())
    dividers = [[[2]], [[6]]]
    packets = list(packets) + dividers
    packets = sorted(packets, key=cmp_to_key(compare))
    out = 1
    for i, packet in enumerate(packets):
        if any(packet == divider for divider in dividers):
            out *= (1 + i)
    print(out)
            
