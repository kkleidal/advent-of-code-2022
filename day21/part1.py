import sys
from collections import defaultdict

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


def main():
    monkey_to_value = {}
    monkey_to_references = defaultdict(set)

    def report_value(monkey):
        if monkey in monkey_to_value:
            node = monkey_to_value[monkey]
            if isinstance(node, (int, float)):
                for ref in sorted(monkey_to_references[monkey]):
                    ref_node = monkey_to_value[ref]
                    assert isinstance(ref_node, OperationNode)
                    value = ref_node.report_value(monkey, node)
                    monkey_to_references[monkey].remove(ref)
                    if value is not None:
                        print(f"Assigning monkey {ref} calculated value {value}")
                        monkey_to_value[ref] = value
                        report_value(ref)

    ROOT = "root"
    for line in sys.stdin:
        line = line.strip()
        monkey, op = line.split(": ")
        parts = op.split(" ")
        if len(parts) == 1:
            monkey_to_value[monkey] = int(parts[0])
            print(f"Assigning monkey {monkey} constant value {parts[0]}")
            report_value(monkey)
        else:
            v1, op, v2 = parts
            monkey_to_value[monkey] = OperationNode(v1, op, v2)
            monkey_to_references[v1].add(monkey)
            monkey_to_references[v2].add(monkey)
            report_value(v1)
            report_value(v2)
        if ROOT in monkey_to_value and isinstance(monkey_to_value[ROOT], (int, float)):
            return monkey_to_value[ROOT]
    assert False


if __name__ == "__main__":
    print(main())
        
        
