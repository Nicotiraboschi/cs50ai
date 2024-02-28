from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
R = Symbol("I am both a knight and a knave.")
knowledge0 = And(
        Not(And(Not(R), AKnight)),
        Not(And(R,Not(And(AKnight,AKnave)))),
        Not(R),
        (Not(And(AKnight,AKnave))),
        Or(AKnight,AKnave)
        )

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
R = Symbol("We are both knaves.")
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    (Not(And(AKnight, AKnave))), (Not(And(BKnight, BKnave))),
    Not(And(R,Not(And(AKnave,BKnave)))),
    Not(And(R,AKnave)),
    And(Not(R),AKnave),
    And(Not(R), Or(AKnight, BKnight))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
RA = Symbol("We are the same kind.")
RB = Symbol("We are of different kinds.")
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    (Not(And(AKnight,AKnave))), 
    (Not(And(BKnight,BKnave))),
    Implication(Not(RA), And(AKnave, BKnight)),
    Implication(Not(RB), And(BKnave, AKnight)),
    Implication(RA, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(RB, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
AR_0 = Symbol("I am a knight.")
AR_1 = Symbol("I am a knave.")
BR_0 = Symbol("A said 'I am a knave'.")
BR_1 = Symbol("C is a knave.")
CR = Symbol("A is a knight.")


knowledge3 = And(
    # they should one of them
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    #  they can't be both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # the statements are either true or false
    Implication(Not(BR_0), Or(AR_0, Not(AR_0))),
    Implication(BR_0, Or(AR_1, Not(AR_1))),
    # they can't be both
    Implication(Not(BR_0), Not(And(AR_0, Not(AR_0)))),
    Implication(BR_0, Not(And(AR_1, Not(AR_1)))),
    # single statements
    Or(BR_0, Not(BR_0)),
    Or(BR_1, Not(BR_1)),
    Or(CR, Not(CR)),
    # can't be both
    Not(And(BR_0, Not(BR_0))),
    Not(And(BR_1, Not(BR_1))),
    Not(And(CR, Not(CR))),
    # if they lie, they are knaves, otherwise they are knights
    Implication(Not(BR_0), Biconditional(Not(AR_0), AKnave)),
    Implication(BR_0, Biconditional(Not(AR_1), AKnave)),
    Biconditional(Not(BR_0), BKnave),
    Biconditional(Not(BR_1), BKnave),
    Biconditional(Not(CR), CKnave),
    
    # MAIN base done
    # check the value of the statements
    Implication(Not(BR_0), Biconditional(AR_0, AKnight)),
    Implication(BR_0, Biconditional(AR_1, AKnave)),
    Biconditional(BR_1, CKnave),
    Implication(CR, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave, AR_0, AR_1, BR_0, BR_1, CR]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
