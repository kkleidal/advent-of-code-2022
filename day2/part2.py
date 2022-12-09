import sys
import enum

class Type(enum.Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

pairs = [
    (Type.ROCK, "A", 1),
    (Type.PAPER, "B", 2),
    (Type.SCISSORS, "C", 3),
]

winners = [
    (Type.ROCK, Type.SCISSORS),
    (Type.PAPER, Type.ROCK),
    (Type.SCISSORS, Type.PAPER),
]

first_to_type = {first: tp for tp, first, _ in pairs}
type_to_score = {tp: score for tp, _, score in pairs}
set_to_winner = {frozenset(grp): grp[0] for grp in winners}

loser = {w: min(s - {w}) for s, w in set_to_winner.items()}
winner = {min(s - {w}): w for s, w in set_to_winner.items()}

total_score = 0
for line in sys.stdin:
    parts = line.strip().split(" ", 1)
    op = first_to_type[parts[0]]

    outcome = parts[1]
    if outcome == "X":
        me = loser[op]
    elif outcome == "Y":
        me = op
    elif outcome == "Z":
        me = winner[op]
        
    score = type_to_score[me]
    if op == me:
        score += 3
    elif set_to_winner[frozenset((op, me))] == me:
        score += 6
    total_score += score
print(total_score)
