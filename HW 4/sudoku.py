'''sudoku.py
Difei Lu, CSE 415, Spring 2017, University of Washington
Instructor: S. Tanimoto
Assignment 4 Option C.2+
Problem: sudoku
'''

# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Sudoku"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Difei Lu']
PROBLEM_CREATION_DATE = "27-APR-2017"


def can_add(s, num, b, c):
    '''Tests whether it's legal to add a number in 
       given cell inside given block.'''
    # Test if given number is valid.
    if num > sudoku_size * sudoku_size and num < 1:
        return False
    # Test if it is a empty cell in given position.
    if s.d[b][c] != 0:
        return False
    # Test if there is repeat numbers in the same row, column and block
    coordinate = get_coordinate(b, c)
    col = coordinate[0]
    row = coordinate[1]
    num_col = get_col(s.d, col)
    num_row = get_row(s.d, row)
    num_block = get_block(s.d, b)
    num_col[row] = num
    num_row[col] = num
    num_block[c] = num
    if repeat_test(num_col) or repeat_test(num_row) or repeat_test(num_block):
        return False
    else:
        return True


def add(s, num, b, c):
    '''Add the number to given location.'''
    news = s.__copy__()
    news.d[b][c] = num
    return news


def repeat_test(l):
    '''If the given list has repeat numbers other than 0.
       Return True if there is any repeat.'''
    count = [0] * sudoku_size * sudoku_size
    for i in l:
        if i > 0:
            count[i - 1] += 1
    for j in count:
        if j > 1:
            return True
    return False


def get_row(lst, row):
    '''Return a list of numbers in the given row.'''
    b_lst = [x + sudoku_size * int(row / sudoku_size) for x in range(sudoku_size)]
    i_lst = [x + sudoku_size * int(row % sudoku_size) for x in range(sudoku_size)]
    result = []
    for i in b_lst:
        for j in i_lst:
            result.append(lst[i][j])
    return result


def get_col(lst, col):
    '''Return a list of numbers in the given column.'''
    init_ind = []
    for i in range(sudoku_size):
        init_ind.append(sudoku_size * i)
    b_lst = [x + int(col / sudoku_size) for x in init_ind]
    i_lst = [x + int(col % sudoku_size) for x in init_ind]
    nums = []
    for i in b_lst:
        for j in i_lst:
            nums.append(lst[i][j])
    return nums


def get_block(lst, block):
    '''Return a list of number in the given block.'''
    return lst[block][:]


def get_coordinate(b, c):
    '''Return the coordinate of given index of block
       and index of cell.'''
    x_c = int(c % sudoku_size)
    y_c = int(c / sudoku_size)
    x_b = int(b % sudoku_size)
    y_b = int(b / sudoku_size)
    x = x_b * sudoku_size + x_c
    y = y_b * sudoku_size + y_c
    return (x, y)


def goal_test(s):
    '''If there is no zeros in the given state then it's a goal.'''
    for b in s.d:
        for c in b:
            if c == 0:
                return False
    return True


def goal_message(s):
    return "Congratulations! The sudoku is solved!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def h_remaining(s):
    '''Return the number of empty spot.'''
    goal_sum = sum([x + 1 for x in range(sudoku_size * sudoku_size)]) \
               * sudoku_size * sudoku_size
    s_sum = 0
    for b in s.d:
        for c in b:
            s_sum += c
    return goal_sum - s_sum


def h_euclidean(s):
    constraint = 0
    for i in range(sudoku_size * sudoku_size):
        c1 = 0
        c2 = 0
        col = get_col(s.d, i)
        row = get_row(s.d, i)
        for j in range(len(col)):
            if col[j] == 0:
                c1 += 1
        for k in range(len(row)):
            if row[k] == 0:
                c2 += 1
        constraint += c1 * c1 + c2 * c2
    return constraint


class State():
    def __init__(self, d):
        self.d = d

    def __str__(self):
        # Produces a brief textual description of a state.
        d = self.d
        txt = "\n"
        divider = ""
        for i in range(2 * sudoku_size * sudoku_size - 1):
            divider += "-"
        divider += "\n"
        row_count = 0
        for x in range(sudoku_size * sudoku_size):
            if row_count != 0 and row_count % sudoku_size == 0:
                txt += divider
            row = get_row(d, x)
            ind_count = 0
            for num in row:
                ind_count += 1
                div = " "
                if ind_count % sudoku_size == 0 \
                        and ind_count / sudoku_size != sudoku_size:
                    div = "|"
                if num == 0:
                    txt += " " + div
                else:
                    txt += str(num) + div
            txt += "\n"
            row_count += 1

        return txt

    def __eq__(self, s2):
        if not (type(self) == type(s2)): return False
        d1 = self.d
        d2 = s2.d
        num_of_index = sudoku_size * sudoku_size
        for a in range(num_of_index):
            for b in range(num_of_index):
                if d1[a][b] != d2[a][b]:
                    return False
        return True

    def __lt__(self, s2):
        d1 = self.d
        d2 = s2.d
        c1 = 0
        c2 = 0
        for n in range(sudoku_size * sudoku_size):
            for m in range(sudoku_size * sudoku_size):
                if d1[n][m] == 0: c1 += 1
                if d2[n][m] == 0: c2 += 1
        return c1 > c2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])
        for x in range(sudoku_size * sudoku_size):
            news.d.append([])
        for i in range(sudoku_size * sudoku_size):
            news.d[i] = self.d[i][:]
        return news


sudoku_size = 3

# Solution: [[7, 1, 2, 6, 9, 3, 8, 4, 5], \
#            [6, 8, 3, 5, 7, 4, 2, 1, 1], \
#            [4, 9, 5, 2, 1, 8, 3, 7, 6], \
#            [4, 6, 9, 5, 2, 7, 3, 8, 1], \
#            [8, 1, 7, 4, 3, 6, 9, 2, 5], \
#            [5, 2, 3, 1, 8, 9, 6, 4, 7], \
#            [9, 5, 4, 1, 7, 6, 2, 3, 8], \
#            [7, 6, 2, 3, 4, 8, 1, 5, 9], \
#            [8, 3, 1, 9, 5, 2, 7, 6, 4]]

INITIAL_STATE = State([[7, 0, 2, 6, 0, 3, 0, 4, 5], \
                       [6, 8, 0, 5, 7, 4, 2, 0, 1], \
                       [4, 0, 5, 0, 0, 8, 3, 7, 0], \
                       [0, 6, 9, 5, 2, 7, 3, 0, 1], \
                       [8, 1, 7, 4, 0, 6, 0, 2, 0], \
                       [0, 2, 0, 1, 0, 9, 6, 0, 7], \
                       [9, 0, 4, 1, 7, 0, 0, 3, 0], \
                       [7, 0, 2, 3, 0, 8, 0, 0, 9], \
                       [8, 0, 1, 0, 5, 2, 7, 0, 4]])

CREATE_INITIAL_STATE = lambda: INITIAL_STATE

move_combinations = []
for a in range(sudoku_size * sudoku_size):
    for b in range(sudoku_size * sudoku_size):
        for num in range(sudoku_size * sudoku_size):
            move_combinations.append([num + 1, a, b])

OPERATORS = [Operator("Add number " + str(comb[0]) + " to block " + str(comb[1]) + ", cell " + str(comb[2]),
                      lambda s, num=comb[0], a=comb[1], b=comb[2]: can_add(s, num, a, b),
                      lambda s, num=comb[0], a=comb[1], b=comb[2]: add(s, num, a, b))
             for comb in move_combinations]

GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)

HEURISTICS = {'h_remaining': h_remaining, 'h_euclidean': h_euclidean}
