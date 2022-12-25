import sys

def snafu_to_decimal(snafu):
    total = 0
    value = 0
    place = 1
    for c in reversed(snafu):
        total += place * int({"-": -1, "=": -2}.get(c, c))
        place *= 5
    return total

def decimal_to_snafu(dec):
    base_5 = []
    place = 1
    while place < dec:
        place *= 5
    while place >= 1:
        base_5.append(dec // place)
        dec %= place
        place //= 5
    for i in reversed(range(1, len(base_5))):
        while base_5[i] > 2:
            base_5[i] -= 5
            base_5[i - 1] += 1
    assert base_5[0] <= 2
    return "".join(str({-1: "-", -2: "="}.get(x, x)) for x in base_5).lstrip("0")

full_total = 0
for line in sys.stdin:
    line = line.strip()
    dec = snafu_to_decimal(line)
    full_total += dec
    print(dec)
print()
print(full_total)
print(decimal_to_snafu(full_total))
    
