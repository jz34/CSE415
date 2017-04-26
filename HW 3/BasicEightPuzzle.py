# Jiawei Zhang   1337686
# CSE 415 HW3 PartII
# Problem2: Basic 8 Puzzle Formulation

# required:
# metadata, initial state, operators,
# __hash__()      __eq__(s)       __copy__()       __str()__


#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['J. Zhang']
PROBLEM_CREATION_DATE = "18-APR-2017"
PROBLEM_DESC = \
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.2.
'''
#</METADATA>


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
        return False # all other conditions cannot move
    except (Exception) as e:
        print(e)


def move(s, distance):
    '''Assume it's legal to make move, this computes the new
       state resulting from exchanging 0 with the number
       distance away from position of 0'''
    news = s.__copy__() # start with a deep copy
    index = s.d.index(0) # position of 0
    news.d[index] = news.d[index + distance]  # replace 0 with target number
    news.d[index + distance] = 0  # replace target number with 0
    return news


def goal_test(s):
    '''If the current state matches the goal state'''
    return s.d == GOAL_STATE


def goal_message(s):
    return "The Basic Eight Puzzle Transport is Triumphant!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)



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
# puzzle0:
# INITIAL_STATE = State([0, 1, 2, 3, 4, 5, 6, 7, 8])
# puzzle1a:
# INITIAL_STATE = State([1, 0, 2, 3, 4, 5, 6, 7, 8])
# puzzle2a:
# INITIAL_STATE = State([3, 1, 2, 4, 0, 5, 6, 7, 8])
# puzzle4a:
INITIAL_STATE = State([1, 4, 2, 3, 7, 0, 6, 8, 5])

CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>


#<OPERATORS>
distance_combinations = [1,-1,3,-3]
OPERATORS = [Operator("Move the number " + str(distance_combinations[dis])
                      + " away from position of 0.",
                      lambda s, dis=dis: can_move(s, dis),
                      # The default value construct is needed
                      # here to capture the values of dis separately
                      # in each iteration of the list comp. iteration.
                      lambda s, dis=dis: move(s, dis))
             for dis in distance_combinations]
#</OPERATORS


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>


#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

