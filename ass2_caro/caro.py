"""
Caro Player
"""
import math

X = "X"
O = "O"
EMPTY = None

class Caro:
    def __init__(self, size, first_player=X):
        """first_player=X
        @Params:
            size: (#_rows, #_cols)
            first_player: X or O as first player
        """
        assert len(size) == 2, "Invalid board size (#_rows, #_cols)"

        self.rows, self.cols = size
        self.board = [[EMPTY] * self.cols for i in range(self.rows)]
        self.first_player = first_player if first_player in [X, O] else X
        self.current_player = self.first_player
        self.winner = None

    def reset(self):
        self.board = [[EMPTY] * self.cols for i in range(self.rows)]
        self.current_player = self.first_player
        self.winner = None

    def next_player(self):
        """
        Returns player who has the next turn on a board.
        """
        return X if self.current_player == X else O

    def terminal(self):
        return False

    def winner(self):
        return self.winner if self.terminal else None

    def result(self, move):
        """
        move: (row, col) -> Update board at pos (row, col)
        """
        x, y = move
        if self.board[x][y] == EMPTY:
            self.board[x][y] = self.current_player
            self.current_player = X if self.current_player == O else O