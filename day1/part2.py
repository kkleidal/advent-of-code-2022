import sys

elves = []
total = 0
for line in sys.stdin:
	line = line.strip()
	if line:
		total += int(line)
	else:
		elves.append(total)
		total = 0
if total:
	elves.append(total)

print(sum(sorted(elves)[-3:]))
		
