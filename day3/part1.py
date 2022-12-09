import sys

priority = 0
for line in sys.stdin:
    line = line.strip()
    if line:
        c = len(line)//2
        common = set(line[:c]) & set(line[c:])
        assert len(common) == 1
        common_letter = min(common)
        if common_letter.isupper():
            priority += ord(common_letter) - ord('A') + 27
        else:
            priority += ord(common_letter) - ord('a') + 1
print(priority)
