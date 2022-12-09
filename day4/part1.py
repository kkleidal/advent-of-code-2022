import sys

fully_contains = 0
for line in sys.stdin:
    pairs = list(map(lambda x: tuple(map(int, x.split("-"))), line.strip().split(",")))
    (s1, e1), (s2, e2) = pairs
    p1 = set(range(s1, e1+1))
    p2 = set(range(s2, e2+1))
    both = p1 & p2
    if p1 == both or p2 == both:
        fully_contains += 1
print(fully_contains)
