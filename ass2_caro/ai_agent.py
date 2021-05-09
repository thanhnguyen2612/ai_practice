import Caro

# Player as AI -> minimize the score
def minimax(state):
    actions = state.actions()
    
    if state.player() == Caro.X:
        scores = [min_value(state.result(action)) for action in actions]
        return actions[scores.index(max(scores))]
    else:
        scores = [max_value(state.result(action)) for action in actions]
        return actions[scores.index(min(scores))]

def max_value(state):
    if state.terminal():
        return state.utility()
    scores = [min_value(state.result(action)) for action in state.actions()]
    return max(scores)

def min_value(state):
    if state.terminal():
        return state.utility()
    scores = [max_value(state.result(action)) for action in state.actions()]
    return min(scores)