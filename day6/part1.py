import sys
from collections import deque

def run(buf_length=4):
    q = deque()
    i = 0
    while True:
        c = sys.stdin.read(1)
        if len(c) == 0:
            break
        if len(q) == buf_length:
            q.popleft()
        q.append(c)
        if len(q) == buf_length and len(set(q)) == buf_length:
            return i + 1
            break
        i += 1

if __name__ == "__main__":
    print(run())
