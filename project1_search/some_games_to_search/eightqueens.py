# Magic block of codes for import package from parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import search
import random

class Action:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.cost = 1
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.cost == other.cost

    def __hash__(self):
        return hash(self.i + 13*self.j + self.cost)

    def __str__(self):
        return f"({self.i}-{self.j})"

class BoardState:
    """
    Implement 8x8 Board for 8 queens
    """
    def __init__(self, size=8):
        self.size = size
        self.queens = set()
    
    def __str__(self):
        s = []
        for i in range(self.size):
            line = '|'
            line += '|'.join('X' if (i, j) in self.queens else ' ' for j in range(self.size))
            line += '|'
            s.append('-' * (self.size * 2 + 1))
            s.append(line)
        s.append('-' * (self.size * 2 + 1))
        return '\n'.join(s)
    
    def __eq__(self, other):
        return self.size == other.size and self.queens == other.queens

    def __hash__(self):
        return hash(str(self.queens))
    
    def isGoal(self):
        return len(self.queens) == self.size
    
    def addQueen(self, queen_pos):
        x, y = queen_pos
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise Exception("Queen out of board")
        if self.isSafe(queen_pos):
            self.queens.add(queen_pos)

    def result(self, action):
        new_board = BoardState(self.size)
        queens = self.queens.copy()
        [new_board.addQueen(queen) for queen in self.queens]
        queen_pos = (action.i, action.j)
        new_board.addQueen(queen_pos)
        return new_board

    def addRandomQueens(self):
        THRESH_HOLD = 50
        counter = 0
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.isSafe((x, y)):
                self.queens.add((x, y))
                return (x, y)
            counter += 1
            if counter == THRESH_HOLD:
                return None
    
    def isSafe(self, queen_pos):
        x, y = queen_pos
        for queen in self.queens:
            if x == queen[0] or y == queen[1] or abs(x - queen[0]) == abs(y - queen[1]):
                return False
        return True
    
    def legalMoves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.isSafe((i, j)):
                    moves.append(Action(i, j))
        return moves

if __name__ == "__main__":
    board = BoardState()
    board.addRandomQueens()
    print('Add a random queen:')
    print(board)
    
    actions = search.dfs(board) 
    print('DFS found a path of %d moves: %s' % (len(actions), [str(action) for action in actions]))
    curr = board
    for queen_pos in actions:
        input("Press return for the next state...")   # wait for key stroke
        curr = curr.result(queen_pos)
        print(curr)