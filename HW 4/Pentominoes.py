# Jiawei Zhang   1337686
# Partner: Difei Lu
# CSE 415 HW4   Option C.2+
# Pentominoes (goal is to fill a 6 by 10 board.)


'''Pentominoes.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''


#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Pentaminoes"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['J. Zhang']
PROBLEM_CREATION_DATE = "26-APR-2017"
PROBLEM_DESC=\
'''Pentominoes is a polyomino of order 5. The goal of a Pentominoes is 
to tile a rectangular box with the pentominoes (12 polygons formed by 5 
equal-sized squares connected edge-to-edge) i.e. cover the rectangle 
without overlap or gaps. In the problem formulation, it is focused on
solving Pentominoes puzzles on 6 x 10 rectangles.

This formulation of the Tower of Hanoi problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.1.
'''
#</METADATA>


#<COMMON_CODE>
def can_put(rectangle, row, col, polygon):
    '''Testes whether it's legal to put the polygon onto
    the position at (row, col), which gives the position
    of top left of the polygon and the rectangle'''
    try:
        polygon_row = len(polygon)
        polygon_col = len(polygon[0])
        # if the polygon will go outside the rectangle
        if polygon_row + row > 6 or polygon_col + col > 10:
            return False
        # if there will be an overlap after placing the rectangle
        for i in range(polygon_row):
            for j in range(polygon_col):
                if polygon[i][j] != 0 and rectangle.d[0][i + row][j + col] != 0:
                    return False
        return True
    except (Exception) as e:
        print(e)


def put(rectangle, row, col, polygon, category):
    '''put the polygon onto the position given by position
    (row, col), which is the position of the top left of 
    the polygon, remove the category where the polygon comes
    from'''
    news = rectangle.__copy__()  # start with a deep copy
    polygon_row = len(polygon)
    polygon_col = len(polygon[0])
    for i in range(polygon_row):
        for j in range(polygon_col):
            if polygon[i][j] != 0:
                news.d[0][i + row][j + col] = polygon[i][j]
    news.d[1].remove(category)
    return news


def goal_test(s):
    '''If the current state reaches a goal state
    i.e. there is no "0" left in the rectangle or 
    there is nothing left in the polygon pool'''
    return len(s.d[1]) == 0

def goal_message(s):
    return "The Pentomminoes puzzle is solved!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def h_hamming(s):
    '''calculate sum of hamming difference from current 
    polygons left in the pool'''
    polygons_left = len(s.d[1])
    return polygons_left



def h_custom(s):
    count = 0
    for row in range(2,4):
        for col in range(10):
            if s.d[0][row][col] == 0:
                count = count + 1
    for row in range(3):
        for col in range(4,6):
            if s.d[0][row][col] == 0:
                count = count + 1
    for row in range(4,6):
        for col in range(4,6):
            if s.d[0][row][col] == 0:
                count = count + 1
    return count/5

def h_zero(s):
    return 0
#</COMMON_CODE>


#<STATE>
class State():
    def __init__(self, d):
        self.d = d

    def __str__(self):
        # Produces a brief textual description of a state.
        rectangle = self.d[0]
        polygons_left = self.d[1]
        txt = ""
        for row in range(6):
            for col in range(10):
                txt = txt + str(rectangle[row][col]) + " "
            txt = txt + "\n"
        txt = txt + str(polygons_left)
        return txt

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        #news = State([[[0 for x in range(10)] for y in range(6)],[]])
        nb = [[0 for x in range(10)] for y in range(6)]
        nl = []
        for row in range(6):
            for col in range(10):
                nb[row][col] = self.d[0][row][col]
        for category in self.d[1]:
            nl.append(category)
        return State([nb,nl])  #ddidididiidid

    def __eq__(self, s2):
        if not (type(self) == type(s2)): return False
        rectangle1 = self.d[0]
        rectangle2 = s2.d[0]
        for row in range(6):
            for col in range(10):
                if rectangle1[row][col] != rectangle2[row][col]:
                    return False
        return True

    def __lt__(self, other):
        return False

    def __hash__(self):
        return str(self.d[0]).__hash__()

#</STATE>


# Polygons are represented by similar characters
# 12 polygons: F L N P Y T U V W Z I X
# F, L, N, P, and Y can be oriented in 8 ways
F = [[[0,'F','F'],['F','F',0],[0,'F',0]],
     [[0,'F',0],['F','F','F'],[0,0,'F']],
     [[0,'F',0],[0,'F','F'],['F','F',0]],
     [['F',0,0],['F','F','F'],[0,'F',0]],
     [['F','F',0],[0,'F','F'],[0,'F',0]],
     [[0,0,'F'],['F','F','F'],[0,'F',0]],
     [[0,'F',0],['F','F',0],[0,'F','F']],
     [[0,'F',0],['F','F','F'],['F',0,0]]]

L = [[['L',0],['L',0],['L',0],['L','L']],
     [['L','L','L','L'],['L',0,0,0]],
     [['L','L'],[0,'L'],[0,'L'],[0,'L']],
     [[0,0,0,'L'],['L','L','L','L']],
     [[0,'L'],[0,'L'],[0,'L'],['L','L']],
     [['L',0,0,0],['L','L','L','L']],
     [['L','L'],['L',0],['L',0],['L',0]],
     [['L','L','L','L'],[0,0,0,'L']]
     ]

N = [[[0,'N'],[0,'N'],['N','N'],['N',0]],
     [['N','N',0,0],[0,'N','N','N']],
     [[0,'N'],['N','N'],['N',0],['N',0]],
     [['N','N','N',0],[0,0,'N','N']],
     [['N',0],['N',0],['N','N'],[0,'N']],
     [[0,'N','N','N'],['N','N',0,0]],
     [['N',0],['N','N'],[0,'N'],[0,'N']],
     [[0,0,'N','N'],['N','N','N',0]]
     ]

P = [[['P','P'],['P','P'],['P',0]],
     [['P','P','P'],[0,'P','P']],
     [[0,'P'],['P','P'],['P','P']],
     [['P','P',0],['P','P','P']],
     [['P','P'],['P','P'],[0,'P']],
     [[0,'P','P'],['P','P','P']],
     [['P',0],['P','P'],['P','P']],
     [['P','P','P'],['P','P',0]]
     ]

Y = [[[0,'Y'],['Y','Y'],[0,'Y'],[0,'Y']],
     [[0,0,'Y',0],['Y','Y','Y','Y']],
     [['Y',0],['Y',0],['Y','Y'],['Y',0]],
     [['Y','Y','Y','Y'],[0,'Y',0,0]],
     [['Y',0],['Y','Y'],['Y',0],['Y',0]],
     [['Y','Y','Y','Y'],[0,0,'Y',0]],
     [[0,'Y'],[0,'Y'],['Y','Y'],[0,'Y']],
     [[0,'Y',0,0],['Y','Y','Y','Y']]
     ]


# T, U, V, W, and Z can be oriented in 4 ways
T = [[['T','T','T'],[0,'T',0],[0,'T',0]],
     [[0,0,'T'],['T','T','T'],[0,0,'T']],
     [[0,'T',0],[0,'T',0],['T','T','T']],
     [['T',0,0],['T','T','T'],['T',0,0]]
     ]

U = [[['U',0,'U'],['U','U','U']],
     [['U','U'],['U',0],['U','U']],
     [['U','U','U'],['U',0,'U']],
     [['U','U'],[0,'U'],['U','U']]
     ]

V = [[['V',0,0],['V',0,0],['V','V','V']],
     [['V','V','V'],['V',0,0],['V',0,0]],
     [['V','V','V'],[0,0,'V'],[0,0,'V']],
     [[0,0,'V'],[0,0,'V'],['V','V','V']]
     ]

W = [[['W',0,0],['W','W',0],[0,'W','W']],
     [[0,'W','W'],['W','W',0],['W',0,0]],
     [['W','W',0],[0,'W','W'],[0,0,'W']],
     [[0,0,'W'],[0,'W','W'],['W','W',0]]
     ]

Z = [[['Z','Z',0],[0,'Z',0],[0,'Z','Z']],
     [[0,0,'Z'],['Z','Z','Z'],['Z',0,0]],
     [[0,'Z','Z'],[0,'Z',0],['Z','Z',0]],
     [['Z',0,0],['Z','Z','Z'],[0,0,'Z']]
     ]

# I can be oriented in 2 ways
I = [[['I'],['I'],['I'],['I'],['I']],
     [['I','I','I','I','I']]
     ]

# X can be oriented in only 1 way
X = [[[0,'X',0],['X','X','X'],[0,'X',0]]]

#<INITIAL_STATE>
'''
INITIAL_RECTANGLE = [['I','P','P','Y','Y','Y','Y','V','V','V'],
                   ['I','P','P','X','Y','L','L','L','L','V'],
                   ['I','P','X','X','X',0,'Z','Z','L','V'],
                   ['I',0,0,'X',0,0,0,'Z','U','U'],
                   ['I',0,0,0,0,0,0,'Z','Z','U'],
                   [0,0,0,0,0,0,0,0,'U','U']
                   ]

INITIAL_POLYGON_POOL = [F,T,W,N]'''


# Puzzle 2
INITIAL_RECTANGLE = [['I','P','P','Y','Y','Y','Y','V','V','V'],
                   ['I','P','P','X','Y','L','L','L','L','V'],
                   ['I','P','X','X','X','F',0,0,'L','V'],
                   ['I',0,0,'X','F','F','F',0,0,0],
                   ['I',0,0,0,0,0,'F',0,0,0],
                   [0,0,0,0,0,0,0,0,0,0]
                   ]
                   
INITIAL_POLYGON_POOL = [T,W,N,U,Z]


INITIAL_STATE = State([INITIAL_RECTANGLE, INITIAL_POLYGON_POOL])
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>



#<OPERATORS>
position_combinations = [(row, col) for row in range(6) for col in range(10)]


def operator_list():
    '''generate every possible operations'''
    li = []
    for category in INITIAL_POLYGON_POOL:
        for polygon in category:
            li.extend([Operator("Move the polygon " + str(polygon) + " onto location at ("
                      + str(row) + ", " + str(col) + ").",
                      lambda rectangle, row=row, col=col, polygon=polygon, category= category:
                      category in rectangle.d[1] and polygon in category and can_put(rectangle,row,col,polygon),
                      lambda rectangle, row=row, col=col, polygon=polygon, category=category:
                      put(rectangle,row,col,polygon,category))
                      for (row, col) in position_combinations])
    return li


OPERATORS = operator_list()
#</OPERATORS>


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>


#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>


#<HEURISTICS>
HEURISTICS = {'heuristic 1': h_hamming, 'heuristic 2': h_custom, 'no heuristic': h_zero}
#</HEURISTICS>