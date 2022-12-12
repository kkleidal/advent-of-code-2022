import sys

def load_ops():
    for line in sys.stdin:
        line = line.strip()
        if line:
            op = line.split(" ")
            op = tuple(op[:1]) + tuple(map(int, op[1:]))
            yield op

def execute(ops):
    register = 1
    for op in ops:
        if op[0] == "addx":
            yield register
            yield register
            register += op[1]
        elif op[0] == "noop":
            yield register
        else:
            raise NotImplementedError

if __name__ == '__main__':
    output = 0
    for i, register in enumerate(execute(load_ops())):
        i += 1
        if i in (20, 60, 100, 140, 180, 220):
            output += i * register
            print(i, register)
    print(output)
