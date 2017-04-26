# Jiawei Zhang   1337686
# CSE 415 HW3 PartII
# Problem3: A-Star Implementation


# Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from queue import PriorityQueue

# DO NOT CHANGE THIS SECTION
if sys.argv == [''] or len(sys.argv) < 2:
    import EightPuzzleWithHeuristics as Problem

    heuristics = lambda s: Problem.HEURISTICS['h_custom'](s)
else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)
    #initial_state = Problem.State(importlib.import_module(sys.argv[3]).CREATE_INITIAL_STATE())  ################## remove after test #####################

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}


# DO NOT CHANGE THIS SECTION
def runAStar():
    # initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()    ############### uncomment this after test ###############
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT) + " states examined.")
    return path, name


# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialize and put first state into
    # priority queue with respective priority
    # add any auxiliary data structures as needed

    OPEN = PriorityQueue()
    CLOSED = []
    g = {}
    g[initial_state] = 0
    OPEN.put((g[initial_state], initial_state))
    BACKLINKS[initial_state] = -1

    while not OPEN.empty():
        S = OPEN.get()
        S = S[1]
        while S in CLOSED:
            S = OPEN.get()
            S = S[1]
        CLOSED.append(S)


        # DO NOT CHANGE THIS SECTION: begining
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
            # DO NOT CHANGE THIS SECTION: end

            # TODO: finish A* implementation
        COUNT += 1
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if new_state not in CLOSED:
                    BACKLINKS[new_state] = S
                    g[new_state] = g[S] + 1
                    OPEN.put((g[new_state] + heuristics(new_state), new_state))


# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = " + str(len(path) - 1))
    return path


if __name__ == '__main__':
    path, name = runAStar()
