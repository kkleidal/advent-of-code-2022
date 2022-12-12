import re
import sys
from dataclasses import dataclass
from typing import List, Callable
from abc import ABC, abstractmethod

def get_lines():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield line

class Expr(ABC):
    @abstractmethod
    def evaluate(self, old):
        ...
    
    def __call__(self, old):
        return self.evaluate(old)
    

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def evaluate(self, old):
        return self.value

class Old(Expr):
    def evaluate(self, old):
        return old

class Arith(Expr):
    op = None

    def __init__(self, expr_left, expr_right):
        self.expr_left = expr_left
        self.expr_right = expr_right

    def evaluate(self, old):
        return self.op(self.expr_left.evaluate(old), self.expr_right.evaluate(old))

class Add(Arith):
    op = lambda _, x, y: x + y

class Sub(Arith):
    op = lambda _, x, y: x - y

class Mult(Arith):
    op = lambda _, x, y: x * y

class Div(Arith):
    op = lambda _, x, y: x / y

def _parse_expr(expr: str) -> Expr:
    if " " in expr:
        tokens = expr.split(" ")
        assert len(tokens) == 3
        return {
            "+": Add,
            "-": Sub,
            "*": Mult,
            "/": Div,
        }[tokens[1]](
            _parse_expr(tokens[0]),
            _parse_expr(tokens[2]),
        )
    elif expr.isnumeric():
        return Literal(int(expr))
    elif expr == "old":
        return Old()

def parse_operation(op: str) -> Callable[[int], float]:
    assert op.startswith("new = ")
    expr = op[len("new = "):]
    return _parse_expr(expr)
    # m = re.match(r"^new = old ([\+\-\*/]) (\d+)$", op)
    # assert m
    # c = int(m.group(2))
    # return {
    #     "+": lambda x: x + c,
    #     "-": lambda x: x - c,
    #     "*": lambda x: x * c,
    #     "/": lambda x: x / c,
    # }[m.group(1)]
    
@dataclass
class Monkey:
    starting_items: List[int]
    operation: Callable[[int], float]
    test: Callable[[float], bool]
    dest_true: int
    dest_false: int

def parse():
    state = 0
    starting_items = None
    operation = None
    test = None
    dest_true = None
    dest_false = None
    first = True

    monkeys = []

    def flush():
        monkeys.append(Monkey(starting_items, operation, test, dest_true, dest_false))

    for line in get_lines():
        if state == 0:
            assert line.startswith("Monkey")
            if first:
                first = False
            else:
                flush()
            state += 1
        elif state == 1:
            assert line.startswith("Starting items")
            starting_items = list(map(int, line.split(" ", 2)[-1].split(", ")))
            state += 1
        elif state == 2:
            assert line.startswith("Operation: ")
            operation = parse_operation(line.split(" ", 1)[1])
            state += 1
        elif state == 3:
            assert line.startswith("Test: divisible by ")
            c = int(line.split(" ", 3)[-1])
            test = (lambda c: lambda x: x % c == 0)(c)
            state += 1
        elif state == 4:
            assert line.startswith("If true: throw to monkey ")
            dest_true = int(line.split(" ", 5)[-1])
            state += 1
        elif state == 5:
            assert line.startswith("If false: throw to monkey ")
            dest_false = int(line.split(" ", 5)[-1])
            state = 0
        else:
            assert False
    flush()

    return monkeys

def simulate_round(monkeys, items_by_monkey=None, verbose=False, inspect_cb=None):
    def printv(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    if items_by_monkey is None:
        items_by_monkey = [list(monkey.starting_items) for monkey in monkeys]
    for mi, monkey in enumerate(monkeys):
        printv(f"Monkey {mi}:")
        new_items = []
        for x in items_by_monkey[mi]:
            printv(f"  Monkey inspects an item with a worry level of {x}.")
            if inspect_cb:
                inspect_cb(mi, x)
            x = monkey.operation(x)
            printv(f"     Op performed to get {x}.")
            x //= 3
            printv(f"     Div 3 to get {x}.")
            x = int(x)
            if monkey.test(x):
                printv(f"     Test true.")
                dest = monkey.dest_true
            else:
                printv(f"     Test false.")
                dest = monkey.dest_false
            printv(f"     Sent to {dest}.")
            if dest == mi:
                new_items.append(x)
            else:
                items_by_monkey[dest].append(x)
        items_by_monkey[mi] = new_items
    return items_by_monkey
        

if __name__ == "__main__":
    verbose = False
    def printv(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    monkeys = parse()
    total_inspects = [0 for _ in monkeys]
    def inspect_cb(mi, x):
        total_inspects[mi] += 1
    items_by_monkey = None
    for rnd in range(20):
        items_by_monkey = simulate_round(monkeys, items_by_monkey, inspect_cb=inspect_cb)
        printv(f"After round {rnd + 1}, the monkeys are holding items with these worry levels:")
        for i, items in enumerate(items_by_monkey):
            printv(f"Monkey {i}: {', '.join(map(str, items))}")
        printv()
    x, y = sorted(total_inspects)[-2:]
    print(x * y)
