
import random
import math
import copy
import time

opp_nickname = ""
m = 0
n = 0
target = 0
bob = ""
my_side = ""
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    board = initial_state[0]
    global m
    global n
    global target
    global my_side
    global opp_nickname

    m = len(board) # rows
    n = len(board[0]) # columns
    target = k
    opp_nickname = opponent_nickname
    my_side = what_side_I_play


def introduce():
    introduction = "Hello, my name is Pepe. I like to  collect the" + "\n" +\
        "dankest memes."
    return introduction

def nickname():
    return "Pepe"

def makeMove(currentState, currentRemark, timeLimit = 10000):
    global opp_nickname
    win_remark = ["Good game", "It'll be over soon...", "Want to play again"]
    advantage_remark = ["Don't mess up", "A foolish blunder indeed", "That was a bad move"]
    normal_remark = ["This is better than I expected", "I think I can win", "Hmm, nice move", "It's just a game no worries"]
    punctuation = ["!", ".", "?"]
    start_time = time.time()
    result = minimax(currentState, timeLimit, start_time, 3)
    new_state = copy.deepcopy(result[1])
    score = result[0]
    rand = random.randint(0, 100)

    new_remark = ""
    if score > 1000: new_remark = random.choice(win_remark)
    elif score <= 1000 and score > 700: new_remark = random.choice(advantage_remark)
    else: new_remark = random.choice(normal_remark)
    if rand % 2 == 0:
        new_remark += " " + opp_nickname
    new_remark += punctuation[rand % 3]
    current_board = currentState[0]
    new_board = new_state[0]
    move = ()
    for i in range(m):
        for j in range(n):
            if current_board[i][j] != new_board[i][j]:
                break
        else:
            continue
        break
    move = (i, j)
    return [[move, new_state], new_remark]

def static_eval(state):
    global my_side
    my_score = score(state, my_side)
    other_score = score(state, other(my_side))
    return my_score - other_score


def score(state, piece_type):
    # check rows
    board = state[0]
    e_val = 0

    row_val = 0
    column_val = 0
    diagonal_val = 0
    anti_diagonal_val = 0

    other_seen_flag = False
    # rows
    for i in range(m):
        row_val = 0
        other_seen_flag = False
        for j in range(n):
            piece = board[i][j]
            if piece == piece_type:
                row_val += 1
            if piece == other(piece_type):
                other_seen_flag = True
                # break
        if not other_seen_flag:
            e_val += 10 ** row_val
    other_seen_flag = False

    # columns
    for k in range(m):
        column_val = 0
        other_seen_flag = False
        for l in range(n):
            piece = board[l][k]
            if piece == piece_type:
                column_val += 1
            if piece == other(piece_type):
                other_seen_flag = True
                # break
        if not other_seen_flag:
            e_val += 10 ** column_val

    other_seen_flag = False

    # diagonals
    for p in range(m+n-1):
        diagonal_val = 0
        other_seen_flag = False
        for q in range(max(p-m+1,0), min(p+1, n)):
            piece = board[m - p + q - 1][q]
            if piece == piece_type:
                diagonal_val += 1
            if piece == other(piece_type):
                other_seen_flag = True
                # break
        if not other_seen_flag:
            e_val += 10 ** diagonal_val

    other_seen_flag = False

    # antidiagonals
    for r in range(m+n-1):
        anti_diagonal_val = 0
        other_seen_flag = False
        for s in range(max(r-m+1, 0), min(r+1, n)):
            piece = board[r-s][s]
            if piece == piece_type:
                anti_diagonal_val += 1
            if piece == other(piece_type):
                other_seen_flag = True
                # break
        if not other_seen_flag:
            e_val += 10 ** anti_diagonal_val
    other_seen_flag = False

    return e_val


def get_moves(state):
    board = state[0]
    piece = state[1]
    new_piece = other(piece)
    move_list = []
    for i in range(m):
        for j in range(n):
            if board[i][j] == ' ':
                new_board = copy.deepcopy(board)
                new_board[i][j] = piece
                move_list.append([new_board, new_piece])
    return move_list

def minimax(state, time_limit, start_time, depth):
    if time.time() - start_time >= time_limit * 0.8:
        return [static_eval(state), state]
    next_state = []
    piece = state[1]
    if depth == 0:
        return [static_eval(state), state]
    if piece == my_side: best_val = -100000000
    else: best_val = 100000000
    for a_state in get_moves(state):
        a_result = minimax(a_state, time_limit, start_time, depth-1)
        score = a_result[0]
        if (piece == my_side and score > best_val) or \
        (piece == other(my_side) and score < best_val):
            best_val = score
            next_state = a_state
    return [best_val, next_state]

def other(which_side):
    if which_side == "X":
        return "O"
    elif which_side == "O":
        return "X"
    else:
        raise Exception("Illegal argument for function other()")
