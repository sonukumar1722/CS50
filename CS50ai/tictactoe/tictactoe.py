"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def unused_tiles(board):
    """
    Return the number of unused tiles.
    """
    return [tile for row in board for tile in row].count(EMPTY)


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if unused_tiles(board) % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 0 or j > 2 or board[i][j] != EMPTY:
        raise IndexError("Action cannot be performed: Invalid tile")

    state = deepcopy(board)
    state[i][j] = player(board)  # mark
    return state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for c in range(3):
        # Checks horizontal matches
        if board[c][0] != EMPTY and board[c][0] == board[c][1] == board[c][2]:
            return board[c][0]
        # Checks vertical matches
        elif board[0][c] != EMPTY and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]

    # Checks diagonal matches
    if board[1][1] != EMPTY:
        for c in range(0, 3, 2):
            if board[0][c] == board[1][1] == board[2][2-c]:
                return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or unused_tiles(board) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    mark = winner(board)
    if mark is None:
        return 0

    return 1 if mark == X else -1


def min_search(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the optional action for the current player on the bord
    """
    if terminal(board):
        return utility(board), None

    value = math.inf
    action = None

    for a in actions(board):
        v, _ = max_search(result(board, a), alpha, beta)

        if v < value:
            value, action = v, a
            beta = min(beta, value)
        if value <= alpha:
            return value, action

    return value, action


def max_search(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the pair result value and optimal action for the maximum player.
    """
    if terminal(board):
        return utility(board), None

    value = -math.inf
    action = None

    for a in actions(board):
        v, _ = min_search(result(board, a), alpha, beta)
        if v > value:
            value, action = v, a
            alpha = max(alpha, value)
        if value >= beta:
            return value, action

    return value, action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    mark = player(board)
    _, action = max_search(board) if mark == X else min_search(board)
    return action
