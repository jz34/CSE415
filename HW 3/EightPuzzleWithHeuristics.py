# Jiawei Zhang   1337686
# CSE 415 HW3 PartII
# Problem4: Implementing and Comparing Heuristics

# required:
# metadata, initial state, operators,
# __hash__()      __eq__(s)       __copy__()       __str()__
# h_euclidean(s), h_hamming(s), h_manhattan(s), and h_custom(s)

import math

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle with Heuristics"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['J. Zhang']
PROBLEM_CREATION_DATE = "18-APR-2017"
PROBLEM_DESC = \
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.2.
'''
#</METADATA>


#<COMMON_CODE>
def can_move(s, distance):
    '''Testes whether it's legal to exchange 0 with the number 
       distance away from position of 0'''
    try:
        li = s.d
        index = li.index(0)  # position of 0
        if index == 0 and (distance == 1 or distance == 3):
            return True
        if index == 1 and (distance == -1 or distance == 1 or distance == 3):
            return True
        if index == 2 and (distance == -1 or distance == 3):
            return True
        if index == 3 and (distance == 1 or distance == -3 or distance == 3):
            return True
        if index == 4 and (distance == -1 or distance == 1 or distance == -3 or distance == 3):
            return True
        if index == 5 and (distance == -1 or distance == -3 or distance == 3):
            return True
        if index == 6 and (distance == 1 or distance == -3):
            return True
        if index == 7 and (distance == -1 or distance == 1 or distance == -3):
            return True
        if index == 8 and (distance == -1 or distance == -3):
            return True
        return False  # all other conditions cannot move

    except (Exception) as e:
        print(e)


def move(s, distance):
    '''Assume it's legal to make move, this computes the new
       state resulting from exchanging 0 with the number
       distance away from position of 0'''
    news = s.__copy__() # start with a deep copy
    index = news.d.index(0) # position of 0
    news.d[index] = news.d[index + distance]  # replace 0 with target number
    news.d[index + distance] = 0 # replace target number with 0
    return news


def goal_test(s):
    '''If the current state matches the goal state'''
    return s.d == GOAL_STATE


def goal_message(s):
    return "The Eight Puzzle Transport with Heuristics is Triumphant!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def h_euclidean(s):
    '''calculate sum of euclidean distances from current postions to
       the goal positions'''
    dis = 0
    for num in s.d:
        curr_index = s.d.index(num)
        goal_index = GOAL_STATE.index(num)
        curr_row = curr_index / 3
        goal_row = goal_index / 3
        curr_column = curr_index % 3
        goal_column = goal_index % 3
        dis += math.sqrt((curr_row - goal_row) ** 2 + (curr_column - goal_column) ** 2)
    return dis


def h_hamming(s):
    '''calculate sum of hamming distances from current postions to
       the goal positions'''
    dis = 0
    for num in s.d:
        if s.d.index(num) != GOAL_STATE.index(num):
            dis += 1
    return dis


def h_manhattan(s):
    '''calculate sum of manhattan distances from current postions to
       the goal positions'''
    dis = 0
    for num in s.d:
        curr_index = s.d.index(num)
        goal_index = GOAL_STATE.index(num)
        curr_row = curr_index / 3
        goal_row = goal_index / 3
        curr_column = curr_index % 3
        goal_column = goal_index % 3
        dis += abs(curr_row - goal_row) + abs(curr_column - goal_column)
    return dis


def h_custom(s):
    '''calculate sum of heuristic distances from current postions to
       the goal positions using my custom algorithm'''
    dis = 0
    dis = 0
    for num in s.d:
        curr_index = s.d.index(num)
        goal_index = GOAL_STATE.index(num)
        curr_row = curr_index / 3
        goal_row = goal_index / 3
        curr_column = curr_index % 3
        goal_column = goal_index % 3
        dis += (abs(curr_row - goal_row) + abs(curr_column - goal_column))/2
    return dis

#</COMMON_CODE>


#<STATE>
class State():
    def __init__(self, d):
        self.d = d

    def __str__(self):
        # Produces a brief textual description of a state.
        d = self.d
        txt = str(d)
        return txt

    def __eq__(self, s2):
        if not (type(self) == type(s2)): return False
        d1 = self.d;
        d2 = s2.d
        return d1 == d2

    def __lt__(self, other):
        if not (type(self) == type(other)): return False
        d1 = self.d
        d2 = other.d
        for i in range(9):
            if d1[i] != d2[i]:
                return d1[i] < d2[i]

    # def __lt__(self,other):
    #    return self.d < other.d

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])
        for num in self.d:
            news.d.append(num)
        return news
#</STATE>

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]

#<INITIAL_STATE>
# puzzle10a:
# INITIAL_STATE = State([4, 5, 0, 1, 2, 3, 6, 7, 8])
# puzzle12a:
# INITIAL_STATE = State([3, 1, 2, 6, 8, 7, 5, 4, 0])
# puzzle14a:
# INITIAL_STATE = State([4, 5, 0, 1, 2, 8, 3, 7, 6])
# puzzle16a:
INITIAL_STATE = State([0, 8, 2, 1, 7, 4, 3, 6, 5])

CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>


#<OPERATORS>
distance_combinations = [1,-1,3,-3]
OPERATORS = [Operator("Move the number " + str(distance_combinations[dis])
                      + " away from position of 0.",
                      lambda s, dis1=dis: can_move(s, dis1),
                      # The default value construct is needed
                      # here to capture the values of dis separately
                      # in each iteration of the list comp. iteration.
                      lambda s, dis1=dis: move(s, dis1))
             for dis in distance_combinations]
#</OPERATORS


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>


#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>


#<HEURISTICS>
HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 'h_manhattan': h_manhattan, 'h_custom': h_custom}
#</HEURISTICS>