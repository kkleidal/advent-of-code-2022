import sys

def parse():
    return [int(line.strip()) for line in sys.stdin]
    

def sgn(x):
    return 1 if x >= 0 else -1

class LinkedListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

def main():
    order = parse()
    order = [x * 811589153 for x in order]
    numbers_to_loc = {v: i for i, v in enumerate(order)}
    print(order)
   
    numbers_to_node = {}
    head = None
    prev = None
    ll = None
    queue = []
    for x in order: 
        ll = LinkedListNode(x)
        queue.append(ll)
        numbers_to_node[x] = ll
        ll.prev = prev
        if prev:
            prev.next = ll
        else:
            head = ll
        prev = ll
    tail = ll
    tail.next = head
    head.prev = tail

    def make_order():
        start = numbers_to_node[0]    
        order = [start.value]
        cur = start.next
        while cur is not start:
            order.append(cur.value)
            cur = cur.next
        return order

    for _ in range(10):
        for cur in queue:
            moves = cur.value % (len(queue) - 1)
            print(f"Move {moves} {moves}")
            for _ in range(abs(moves)):
                prev = cur.prev
                nxt = cur.next
                if moves < 0:
                    prev.next = nxt
                    nxt.prev = prev

                    cur.prev = prev.prev
                    cur.next = prev
        
                    prev.prev = cur
                    cur.prev.next = cur
                else:
                    cur.next = nxt.next
                    nxt.next.prev = cur

                    cur.prev = nxt
                    nxt.next = cur

                    nxt.prev = prev
                    prev.next = nxt
    # print(make_order())
    
    order = make_order()
    gc_offsets = [1000, 2000, 3000]
    gcs = [order[offset % len(order)] for offset in gc_offsets]
    print(gcs)
    print(sum(gcs))
    # Answer: 8798438007673


if __name__ == "__main__":
    main()
