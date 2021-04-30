import caro

state = caro.CaroState.loadState((12, 12), {(3,4), (3,5), (4,5)}, {(3,3), (3,2)})

Xs = {(1,1), (1,2), (1,3), (1,4), (1,5)}
Os = {(0,1), (1,0), (1,7), (4,4), (5,5)}
x_win_state = caro.CaroState.loadState((12, 12), Xs, Os)
game = caro.CaroGame.loadState(x_win_state)
game.checkWinner()

x_win_state.printBoard()
# print(game.winner())

game2 = caro.CaroGame((12, 12))
for X, O in zip(Xs, Os):
    game2.makeMove(X)
    if game2.terminal():
        print(game2.winner())
        continue
    game2.makeMove(O)
    if game2.terminal():
        print(game2.winner())
        continue