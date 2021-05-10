import re

X = "X"
O = "O"
EMPTY = "."

def evalPattern(repr, player):
    """
    @Params:
        repr: Get ASCII representation of a direction
    @Return:
        evaluation score of the pattern
    """
    if X not in repr and O not in repr: return 0
    def scorePattern(repr, pattern, player):
        if len(pattern.group(0)) < 5:
            return 0
        elif len(pattern.group(0)) == 5:
            s, e = pattern.start(), pattern.end()
            if s > 0 and e < len(repr):
                if repr[s - 1] != player and repr[e] != player:
                    return 0

        # Score barem
        consec_scores = (2, 5, 1000, 10000)
        block_weight = (0.5, 0.6, 0.01, 0.25)

        p_str = pattern.group(0)
        score, cons = 0, 0

        # Count for number of consecutive
        block = True
        for p in p_str:
            if p != EMPTY:
                cons += 1
            elif cons > 0 and cons < 5:
                if block:
                    score += consec_scores[cons - 1] * block_weight[cons - 1]
                    block = False
                else:
                    score += consec_scores[cons - 1]
                cons = 0
            else:
                block = False
                cons = 0

        # Last mark is PLAYER
        if cons > 0 and cons < 5:
            if e < len(repr):
                score += consec_scores[cons - 1] * block_weight[cons - 1]
            else:
                score += consec_scores[cons - 1]

        return score

    weight = (0.3, 0.7)     # Weight on current player

    # Score X
    X_ext = re.compile(r"[X.]+")
    eval_X = 0
    for pattern in X_ext.finditer(repr):
        eval_X += scorePattern(repr, pattern, X)
        print("Eval_X", eval_X)
    
    # Score O
    O_ext = re.compile(r"[O.]+")
    eval_O = 0
    for pattern in O_ext.finditer(repr):
        eval_O -= scorePattern(repr, pattern, O)
        print("Eval_O", eval_O)

    eval_score = eval_X * weight[player == X] + eval_O * weight[player == O]
    return eval_score

# s = "..XX.OO.X..XO"
s = "..XXXO.."
print(evalPattern(s, O))