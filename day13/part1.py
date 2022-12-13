import ast
import sys

def parse():
    pair = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            pair.append(ast.literal_eval(line))
            if len(pair) == 2:
                yield pair
                pair = []
    if len(pair) == 2:
        yield pair
        pair = []
    assert len(pair) == 0

def compare(left, right):
    if isinstance(left, list) and isinstance(right, list):
        for xl, xr in zip(left, right):
            cmp = compare(xl, xr)
            if cmp < 0:
                return -1
            elif cmp > 0:
                return 1
        if len(left) < len(right):
            return -1
        elif len(left) == len(right):
            return 0
        else:
            return 1
    elif isinstance(left, list):
        return compare(left, [right])
    elif isinstance(right, list):
        return compare([left], right)
    else:
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1
        

if __name__ == "__main__":
    score = 0
    for i, (left, right) in enumerate(parse()):
        if compare(left, right) == -1:
            score += (i + 1)
    print(score)
