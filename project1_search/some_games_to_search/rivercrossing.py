# Magic block of codes for import package from parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import search

class Action:
    def __init__(self, i):
        self.i = i
        self.cost = 1
    def __eq__(self, other):
        return self.i == other.i and self.cost == other.cost
    def __str__(self):
        return str(i)
class RiverCrossingState:
    """
    Implement state of farmer game: 4 characters (farmer, wolf, goat, cabbage)
    @Rules:
        1. Woft & Goat cannot be together without farmer
        2. Goat & Cabbage cannot be together without farmer
        3. Boat always for 2: farmer & one thing
    """
    CHARS = ["Farmer", "Wolf", "Goat", "Cabbage"]
    def __init__(self):
        """
        List represents bitmap for the presence of 4 characters on each riverside
        [Farmer, Wolf, Goat, Cabbage]
        """
        self.riverside = [1, 1, 1, 1]      # All at riverside 1
    
    def __eq__(self, other):
        return self.riverside == other.riverside
    
    def __hash__(self):
        return hash(str(self.riverside))
    
    def __str__(self):
        result = []
        r1 = '-'.join(char if bit else '-'*len(char) for bit, char in zip(self.riverside, self.CHARS))
        r2 = '-'.join(char if bit else '-'*len(char) for bit, char in zip(self.otherSide(), self.CHARS))

        result.append('=' * 25)
        result.append(r1)
        result.append('~ ' * 12)
        result.append(' ~' * 12)
        result.append(r2)
        result.append('=' * 25)

        return "\n".join(result)
    
    def isGoal(self):
        return self.riverside == [0, 0, 0, 0]
    
    def otherSide(self):
        return list(map(lambda x: int(not x), self.riverside))
    
    def isSafe(self):
        if self.riverside[1] == self.riverside[2] and self.riverside[0] != self.riverside[1]:
            # Wolf and Goat be together without the Farmer
            return False
        elif self.riverside[2] == self.riverside[3] and self.riverside[0] != self.riverside[2]:
            # Goat and Cabbage be together without the Farmer
            return False
        return True
    
    def legalMoves(self):
        return [Action(i) for i, bit in enumerate(self.riverside) 
                    if bit == self.riverside[0]
                        and self.result(Action(i)).isSafe()]
    
    def result(self, action):
        """
        Index of the character bring to the otherside
        """
        char_idx = action.i
        if self.riverside[0] != self.riverside[char_idx]:
            raise Exception(f"{self.CHARS[char_idx]} cannot boat by itself")

        new_game = RiverCrossingState()
        new_game.riverside = self.riverside.copy()

        # From this riverside
        if new_game.riverside[0] == 1:
            new_game.riverside[0] = max(new_game.riverside[0] - 1, 0)
            new_game.riverside[char_idx] = max(new_game.riverside[char_idx] - 1, 0)
        # From the other side go back
        else:
            new_game.riverside[0] = min(new_game.riverside[0] + 1, 1)
            new_game.riverside[char_idx] = min(new_game.riverside[char_idx] + 1, 1)
        return new_game
    
if __name__ == "__main__":
    puzzle = RiverCrossingState()
    
    # problem = RiverCrossingProblem(puzzle)
    actions = search.bfs(puzzle)
    # print('BFS found a path of %d moves: %s' % (len(actions), str(actions)))
    
    curr = puzzle
    for action in actions:
        input("Press return for the next state...")   # wait for key stroke
        curr = curr.result(action)
        print(curr)