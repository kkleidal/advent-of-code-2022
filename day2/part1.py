import sys
import enum

class Type(enum.Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

pairs = [
    (Type.ROCK, "A", "X", 1),
    (Type.PAPER, "B", "Y", 2),
    (Type.SCISSORS, "C", "Z", 3),
]

winners = [
    (Type.ROCK, Type.SCISSORS),
    (Type.PAPER, Type.ROCK),
    (Type.SCISSORS, Type.PAPER),
]

first_to_type = {first: tp for tp, first, _, _ in pairs}
second_to_type = {second: tp for tp, _, second, _ in pairs}
type_to_score = {tp: score for tp, _, _, score in pairs}
set_to_winner = {frozenset(grp): grp[0] for grp in winners}

total_score = 0
for line in sys.stdin:
    parts = line.strip().split(" ", 1)
    op = first_to_type[parts[0]]
    me = second_to_type[parts[1]]
    score = type_to_score[me]
    if op == me:
        score += 3
    elif set_to_winner[frozenset((op, me))] == me:
        score += 6
    total_score += score
print(total_score)
