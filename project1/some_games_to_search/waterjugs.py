# Magic block of codes for import package from parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import search

class Action:
    def __init__(self, from_jug, to_jug):
        self.from_jug = from_jug
        self.to_jug = to_jug
        self.cost = 1

    def __hash__(self):
        return hash(self.from_jug + 13*self.to_jug)

    def __eq__(self, other):
        return self.from_jug == other.from_jug and self.to_jug == other.to_jug
    
    def __str__(self):
        return f"{self.from_jug}=>{self.to_jug}"

class WaterJug:
    def __init__(self, capacity, water=0):
        self.water = water
        self.capacity = capacity
    
    def __str__(self):
        return f"({self.water}/{self.capacity})"

    def __hash__(self):
        return hash(self.water + 13 * self.capacity)

    def __eq__(self, other):
        return self.water == other.water and self.capacity == other.capacity

    def isEmpty(self):
        return self.water == 0

    def isFull(self):
        return self.water == self.capacity
    
    def pour_in(self, water):
        remainder = max(self.water + water - self.capacity, 0)
        self.water = min(self.water + water, self.capacity)

        # Return water's remainder
        return remainder
    
    def pour_to(self, other_jug):
        self.water = other_jug.pour_in(self.water)
    
    def copy(self):
        return WaterJug(self.capacity, self.water)

class WaterJugsState:
    def __init__(self):
        self.jugs = [WaterJug(8, 8), WaterJug(5), WaterJug(3)]
    
    def __str__(self):
        return ' - '.join(str(jug) for jug in self.jugs)
    
    def __eq__(self, other):
        return self.jugs == other.jugs
    
    def __hash__(self):
        return sum(hash(jug) for jug in self.jugs)
    
    def isGoal(self):
        return self.jugs == [WaterJug(8, 4), WaterJug(5, 4), WaterJug(3)]
    
    def legalMoves(self):
        # Return a list of states, each state in format (<from_jug_idx>, <to_jug_idx>)
        moves = set()
        for i in range(3):
            if self.jugs[i].isEmpty(): continue
            for j in range(3):
                if i == j or self.jugs[j].isFull(): continue
                moves.add(Action(i, j))
        return moves
    
    def result(self, action):
        from_jug, to_jug = action.from_jug, action.to_jug
        new_state = WaterJugsState()
        new_state.jugs = [jug.copy() for jug in self.jugs]
        new_state.jugs[from_jug].pour_to(new_state.jugs[to_jug])
        return new_state
        
if __name__ == '__main__':
    water_jugs = WaterJugsState()
    
    # problem = WaterJugsProblem(water_jugs)
    actions = search.bfs(water_jugs)
    # print('BFS found a path of %d moves: %s' % (len(actions), str(actions)))
    print(f"Start: \t\t {water_jugs}")
    curr = water_jugs
    for action in actions:
        curr = curr.result(action)
        print(f"Pour {action}:\t", curr)