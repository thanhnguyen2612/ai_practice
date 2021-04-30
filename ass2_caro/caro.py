"""
Caro Player
"""
import math
import re

X = "X"
O = "O"
EMPTY = "."

# Enumeration of checking winning directions
HORIZONTAL = 0
VERTICAL = 1
DIAGONAL_L = 2
DIAGONAL_R = 3

SCORE = {X: 1, O: -1, EMPTY: 0}

class CaroState:
    def __init__(self, size):
        self.n_rows, self.n_cols = size
        self.X_moves = set()
        self.O_moves = set()

    @classmethod
    def loadState(cls, size, Xs, Os):
        new_state = cls(size)
        new_state.X_moves = Xs
        new_state.O_moves = Os
        return new_state
    
    def __eq__(self, other):
        if self.n_rows != other.n_rows or \
           self.n_cols != other.n_cols or \
           self.X_moves != other.X_moves or \
           self.O_moves != other.O_moves:
            return False
        return True
    
    def __hash__(self):
        h = hash(self.n_rows + 13 * self.n_cols)
        x_hash = hash(str(self.X_moves))
        o_hash = hash(str(self.O_moves))
        return x_hash + o_hash + h
    
    def copy(self):
        copyState = CaroState.loadState((self.n_rows, self.n_cols),
                                        self.X_moves.copy(), self.O_moves.copy())
        return copyState

    def printBoard(self):
        [print(self.getASCIIRepr((i,0), HORIZONTAL)) for i in range(self.n_rows)]

    def getBoard(self):
        board = [[EMPTY] * self.n_cols for i in range(self.n_rows)]
        for X_move in self.X_moves:
            board[X_move[0]][X_move[1]] = X
        for O_move in self.O_moves:
            board[O_move[0]][O_move[1]] = O
        return board
    
    def legalMoves(self):
        return [(i, j) for i in range(self.n_rows)
                            for j in range(self.n_cols)
                                if (i, j) not in self.X_moves.union(self.O_moves)]
    
    def markedMoves(self):
        return self.X_moves.union(self.O_moves)

    def player(self):
        return O if len(self.X_moves) > len(self.O_moves) else X

    def result(self, move):
        if move in self.X_moves or move in self.O_moves:
            return
        new_state = self.copy()
        if self.player() == X:
            new_state.X_moves.add(move)
        else:
            new_state.O_moves.add(move)
        return new_state
    
    def getASCIIRepr(self, pos, dir):
        """
        Get string patterns along a direction
        @Params:
            pos: (x, y) 2D-position
            dir: HORIZONTAL/VERTICAL/DIAGONAL_L/DIAGONAL_R
        """
        x, y = pos
        result = ""
        if dir == HORIZONTAL:
            for col in range(self.n_cols):
                if (x, col) in self.X_moves:
                    result += X
                elif (x, col) in self.O_moves:
                    result += O
                else:
                    result += EMPTY
        elif dir == VERTICAL:
            for row in range(self.n_rows):
                if (row, y) in self.X_moves:
                    result += X
                elif (row, y) in self.O_moves:
                    result += O
                else:
                    result += EMPTY
        elif dir == DIAGONAL_L:
            i, j = x - min(x, y), y - min(x, y)
            while i < self.n_rows and j < self.n_cols:
                if (i, j) in self.X_moves:
                    result += X
                elif (i, j) in self.O_moves:
                    result += O
                else:
                    result += EMPTY
                i, j = i + 1, j + 1
        elif dir == DIAGONAL_R:
            i, j = x - min(x, y), y + min(x, y)
            while i < self.n_rows and j >= 0:
                if (i, j) in self.X_moves:
                    result += X
                elif (i, j) in self.O_moves:
                    result += O
                else:
                    result += EMPTY
                i, j = i + 1, j - 1
        return result

class CaroGame:
    def __init__(self, size):
        assert len(size) == 2, "Invalid board size (#_rows, #_cols)"

        self.n_rows, self.n_cols = size     # n_rows, n_cols: # of rows & cols, respectively
        self.state = CaroState(size)        # state: current state of caro game
        self._winner = None                 # _winner: X or O, None if not yet
        self.board = self.state.getBoard()
    
    @classmethod
    def loadState(self, state):
        game = CaroGame((state.n_rows, state.n_cols))
        game.state = state
        game.board = game.state.getBoard()
        return game

    def getGameState(self):
        return CaroState((self.n_rows, self.n_cols))
    
    def getBoard(self):
        return self.board

    def reset(self):
        self.state = CaroState((self.n_rows, self.n_cols))
        self._winner = None
        self.board = self.state.getBoard()

    def nextPlayer(self):
        """
        Returns player who has the next turn on a board.
        """
        return self.state.player()

    def terminal(self):
        if self._winner is not None:
            return True
        
        if len(self.state.markedMoves()) < (self.n_rows * self.n_cols):
            return False
        return True
    
    def winner(self):
        return self._winner
    
    def _checkWinByMove(self, move, dir):
        """
        checkWin in a direction
        @Params:
            move: (x, y) 2D-position of move
        @Return:
            True if winning satisfied
            X/O returned to know who is the winner
        """
        repr = self.state.getASCIIRepr(move, dir)
        patterns = [p for p in repr.split(EMPTY) if p]
        X_checker = re.compile(r"(^X{5}O.*)|(.*OX{5}$)|(X{5})")
        O_checker = re.compile(r"(^O{5}X.*)|(.*XO{5}$)|(O{5})")

        for p in patterns:
            if X_checker.fullmatch(p):
                self._winner = X
                return True
            elif O_checker.fullmatch(p):
                self._winner = O
                return True
        return False

    def checkWinnerByMove(self, move):
        if self._checkWinByMove(move, HORIZONTAL): return
        if self._checkWinByMove(move, VERTICAL): return
        if self._checkWinByMove(move, DIAGONAL_L): return
        if self._checkWinByMove(move, DIAGONAL_R): return
    
    def checkWinner(self):
        for i in range(self.n_rows):
            if self._checkWinByMove((i, 0), HORIZONTAL): return self._winner
        for i in range(self.n_cols):
            if self._checkWinByMove((0, j), VERTICAL): return self._winner

        return None

    def makeMove(self, move):
        """
        move: (row, col) -> Update board at pos (row, col)
        """
        x, y = move
        player = self.state.player()
        self.state = self.state.result(move)
        self.board[x][y] = player
        self.checkWinnerByMove(move)