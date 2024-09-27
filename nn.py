import chess
import chess.engine
import random
import numpy as np
def conv_state(state):
    new_state=np.zeros(8,8,dtype)
    pass
def random_board(max_depth=200):
    board=chess.Board()
    depth=random.randrange(0,max_depth)

    for _ in range(depth):
        all_moves=list(board.legal_moves)
        random_move=random.choice(all_moves)
        board.push(random_move)
        if board.is_game_over():
            break
    return board

state=random_board(1)
print(state)