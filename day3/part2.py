import sys

def get_lines():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield line

def group_by(it, num):
    grp = []
    for line in it:
        grp.append(line)
        if len(grp) == num:
            yield grp
            grp = []
    if len(grp) == num:
        yield grp

def intersect(it):
    out = None
    for x in it:
        if out is None:
            out = x
        else:
            out &= x
    return out

priority = 0
for group in group_by(get_lines(), 3):
    common = intersect(set(bag) for bag in group)
    assert len(common) == 1
    common_letter = min(common)
    if common_letter.isupper():
        priority += ord(common_letter) - ord('A') + 27
    else:
        priority += ord(common_letter) - ord('a') + 1
print(priority)
