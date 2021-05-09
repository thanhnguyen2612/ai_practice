"""
Caro Player
"""
import math
import re

X = "X"
O = "O"
EMPTY = "."

WIN = 3             # Number of consecutive marks to win

# Enumeration of checking winning directions
HORIZONTAL = 0
VERTICAL = 1
DIAGONAL_L = 2      # From top-left down to bottom-right
DIAGONAL_R = 3      # From top-right down to bottom-left

SCORE = {X: 1, O: -1, EMPTY: 0}

class CaroState:
    def __init__(self, size):
        assert len(size) == 2, "Invalid board size (#_rows, #_cols)"
        assert size[0] >= WIN and size[1] >= WIN, "Invalid caro game"
        self.n_rows, self.n_cols = size
        self.X_moves = set()
        self.O_moves = set()
        self._winner = None     # Cache the winner: X/O or None if not yet

    @classmethod
    def loadState(cls, size, Xs, Os, player_win=None):
        new_state = cls(size)
        new_state.X_moves = Xs
        new_state.O_moves = Os
        new_state._winner = player_win
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
        copyState = CaroState.loadState((self.n_rows, self.n_cols), self.X_moves.copy(), 
                                         self.O_moves.copy(), self._winner)
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
    
    def markedMoves(self):
        return self.X_moves.union(self.O_moves)
    
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
    
    def _checkWinByPos(self, pos, dir):
        """
        checkWin in a direction
        @Params:
            move: (x, y) 2D-position of move
        @Return:
            True if winning satisfied
            X/O returned to know who is the winner
        """
        repr = self.getASCIIRepr(pos, dir)
        patterns = [p for p in repr.split(EMPTY) if p]
        X_checker = re.compile(f"(^X{{{WIN}}}O.*)|(.*OX{{{WIN}}}$)|(X{{{WIN}}})")
        O_checker = re.compile(f"(^O{{{WIN}}}X.*)|(.*XO{{{WIN}}}$)|(O{{{WIN}}})")

        for p in patterns:
            if X_checker.fullmatch(p):
                return X
            elif O_checker.fullmatch(p):
                return O
        return None

    def player(self):
        return O if len(self.X_moves) > len(self.O_moves) else X
    
    def actions(self):
        return [(i, j) for i in range(self.n_rows)
                            for j in range(self.n_cols)
                                if (i, j) not in self.X_moves.union(self.O_moves)]

    def result(self, move):
        if move in self.X_moves or move in self.O_moves:
            return
        new_state = self.copy()
        if self.player() == X:
            new_state.X_moves.add(move)
        else:
            new_state.O_moves.add(move)
        return new_state

    def winner(self):
        if self._winner is not None: return self._winner        # Return value from cache

        # Check all rows
        for i in range(self.n_rows):
            player_win = self._checkWinByPos((i, 0), HORIZONTAL)
            if player_win is not None:
                self._winner = player_win
                return player_win

        # Check all columns
        for i in range(self.n_cols):
            player_win = self._checkWinByPos((0, i), VERTICAL)
            if player_win is not None:
                self._winner = player_win
                return player_win

        # Check all diagonal left
        for i in range(self.n_rows + self.n_cols - WIN * 2 + 1):
            player_win = self._checkWinByPos((i, self.n_cols - WIN), DIAGONAL_L)
            if player_win is not None:
                self._winner = player_win
                return player_win

        # Check all diagonal right
        for i in range(self.n_rows + self.n_cols - WIN * 2 + 1):
            player_win = self._checkWinByPos((i, WIN - 1), DIAGONAL_R)
            if player_win is not None:
                self._winner = player_win
                return player_win
        return None

    def terminal(self):
        if self.winner() is not None:
            return True
        if len(self.markedMoves()) < (self.n_rows * self.n_cols):
            return False
        return True

    def utility(self):
        player_win = self.winner()
        if player_win == X:
            return 1
        elif player_win == O:
            return -1
        return 0

class CaroGame:
    def __init__(self, size):
        assert len(size) == 2, "Invalid board size (#_rows, #_cols)"
        assert size[0] >= WIN and size[1] >= WIN, "Invalid caro game"

        self.n_rows, self.n_cols = size     # n_rows, n_cols: # of rows & cols, respectively
        self.state = CaroState(size)        # state: current state of caro game
        self.board = self.state.getBoard()
    
    @classmethod
    def loadState(self, state):
        game = CaroGame((state.n_rows, state.n_cols))
        game.state = state
        game.board = game.state.getBoard()
        return game

    def getStartState(self):
        return CaroState((self.n_rows, self.n_cols))
    
    def getBoard(self):
        return self.board

    def reset(self):
        self.state = CaroState((self.n_rows, self.n_cols))
        self.board = self.state.getBoard()

    def nextPlayer(self):
        """
        Returns player who has the next turn on a board.
        """
        return self.state.player()

    def terminal(self):
        if self.state.winner() is not None:
            return True
        
        if len(self.state.markedMoves()) < (self.n_rows * self.n_cols):
            return False
        return True
    
    def winner(self):
        return self.state.winner()

    def makeMove(self, move):
        """
        move: (row, col) -> Update board at pos (row, col)
        """
        x, y = move
        player = self.state.player()
        self.state = self.state.result(move)
        self.board[x][y] = player
    
    def legalMoves(self):
        """
        Return all possible actions (i, j) available on board.
        """
        return self.state.actions()