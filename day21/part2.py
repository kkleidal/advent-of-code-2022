import sys
from collections import defaultdict
from abc import abstractmethod

class Expr:
    @abstractmethod
    def pretty_print(self, indent=0):
        ...

    @abstractmethod
    def is_constant(self):
        ...

    @abstractmethod
    def eval_constant(self):
        ...

class Literal(Expr):
    def __init__(self, value: int):
        self.value = value

    def pretty_print(self, indent=0):
        print((" " * indent) + ("Literal: %d" % self.value))

    def is_constant(self):
        return True

    def eval_constant(self):
        return self.value
    

class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def pretty_print(self, indent=0):
        print((" " * indent) + ("Variable: %s" % self.name))

    def is_constant(self):
        return False

    def eval_constant(self):
        raise ValueError("Not constant")

class BinaryOp(Expr):
    symbol = None
    def __init__(self, lhs: Expr, rhs: Expr):
        self.lhs = lhs
        self.rhs = rhs

    @classmethod
    @abstractmethod
    def apply(cls, x, y):
        ...

    def pretty_print(self, indent=0):
        print((" " * indent) + ("%s:" % type(self).__name__))
        self.lhs.pretty_print(indent + 2)
        self.rhs.pretty_print(indent + 2)

    def is_constant(self):
        return self.lhs.is_constant() and self.rhs.is_constant()

    def eval_constant(self):
        return self.apply(self.lhs.eval_constant(), self.rhs.eval_constant())
        
        
class Add(BinaryOp):
    symbol = "+"

    @classmethod
    def apply(cls, x, y):
        return x + y

class Sub(BinaryOp):
    symbol = "-"

    @classmethod
    def apply(cls, x, y):
        return x - y

class Mult(BinaryOp):
    symbol = "*"

    @classmethod
    def apply(cls, x, y):
        return x * y

class Div(BinaryOp):
    symbol = "/"

    @classmethod
    def apply(cls, x, y):
        return x // y

class OperationNode:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.lhs_value = None
        self.rhs_value = None
        self.my_value = None

    def report_value(self, monkey, value):
        if monkey == self.lhs:
            self.lhs_value = value
        if monkey == self.rhs:
            self.rhs_value = value
        if self.lhs_value is not None and self.rhs_value is not None:
            self.my_value = {
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x // y,
            }[self.op](self.lhs_value, self.rhs_value)
            return self.my_value
        return None


ROOT = "root"
VARIABLE = "humn"

def parse():
    monkey_to_value = {}
    for line in sys.stdin:
        line = line.strip()
        monkey, op = line.split(": ")
        parts = op.split(" ")
        if monkey == VARIABLE:
            monkey_to_value[monkey] = None
        elif len(parts) == 1:
            monkey_to_value[monkey] = int(parts[0])
        else:
            v1, op, v2 = parts
            monkey_to_value[monkey] = (v1, op, v2)
    return monkey_to_value

def build_tree(monkey_to_value):
    def build_node(name):
        value = monkey_to_value[name]
        if isinstance(value, int):
            return Literal(value)
        elif value is None:
            return Variable(VARIABLE)
        else:
            return {
                '+': Add,
                '-': Sub,
                '*': Mult,
                '/': Div,
            }[value[1]](
                build_node(value[0]),
                build_node(value[2]),
            )
    return build_node(ROOT)

def main():
    monkey_to_value = parse()
    root = build_tree(monkey_to_value)
    lhs = root.lhs
    rhs = root.rhs


    lhs_constant = lhs.is_constant() 
    rhs_constant = rhs.is_constant()
    
    assert lhs_constant != rhs_constant

    constant_side = lhs if lhs_constant else rhs
    vs = rhs if lhs_constant else lhs
    constant_side_value = constant_side.eval_constant()

    # print("Variable side:")
    # vs.pretty_print()
    # print()

    # print("Constant side:")
    # constant_side.pretty_print()
    # print()
    # print("Constant side value: %d" % constant_side_value)

    # Progressively try to simplify variable side:
    while not isinstance(vs, Variable):
        if isinstance(vs, Div):
            if vs.rhs.is_constant():
                constant_side_value *= vs.rhs.eval_constant()
                vs = vs.lhs
            else:
                raise NotImplementedError
        elif isinstance(vs, Mult):
            if vs.lhs.is_constant():
                constant_side_value //= vs.lhs.eval_constant()
                vs = vs.rhs
            elif vs.rhs.is_constant():
                constant_side_value //= vs.rhs.eval_constant()
                vs = vs.lhs
            else:
                raise NotImplementedError
        elif isinstance(vs, Sub):
            if vs.lhs.is_constant():
                constant_side_value = vs.lhs.eval_constant() - constant_side_value
                vs = vs.rhs
            elif vs.rhs.is_constant():
                constant_side_value += vs.rhs.eval_constant()
                vs = vs.lhs
            else:
                raise NotImplementedError
        elif isinstance(vs, Add):
            if vs.lhs.is_constant():
                constant_side_value -= vs.lhs.eval_constant()
                vs = vs.rhs
            elif vs.rhs.is_constant():
                constant_side_value -= vs.rhs.eval_constant()
                vs = vs.lhs
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    # print("Variable side:")
    # vs.pretty_print()
    # print()
    # print("Constant side value: %d" % constant_side_value)
    return constant_side_value
        



if __name__ == "__main__":
    print(main())
