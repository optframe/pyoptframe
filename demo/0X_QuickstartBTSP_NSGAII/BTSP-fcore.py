# OptFrame Python Demo BTSP - Bi-objective Traveling Salesman Problem

# DO NOT REORDER 'import sys ...'
# ****** REMOVE THIS BLOCK IF YOU HAVE INSTALLED OPTFRAME LIBRARY ******
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
# **********************************************************************

import optframe

from optframe import *
from optframe.protocols import *
class SolutionTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n : int = 0
        # visited cities as a list
        self.cities : List[int] = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionTSP(n={self.n};cities={self.cities})"
    
import math

class ProblemContextBTSP(object):
    def __init__(self):
        print('Init BTSP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of cities
        self.n = 0
        # x coordinates for obj 0
        self.vx0 = []
        # y coordinates for obj 0
        self.vy0 = []
        # distance matrix for obj 0
        self.dist0 = []
        # x coordinates for obj 1
        self.vx1 = []
        # y coordinates for obj 1
        self.vy1 = []
        # distance matrix for obj 1
        self.dist1 = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx0.append(int(id_x_y[1]))
               self.vy0.append(int(id_x_y[2]))
            for i in range(self.n):
               id_x_y = lines[self.n+i+1].split()
               # ignore id_x_y[0]
               self.vx1.append(int(id_x_y[1]))
               self.vy1.append(int(id_x_y[2]))
            #
            self.dist0 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist0[i][j] = round(self.euclidean(self.vx0[i], self.vy0[i], self.vx0[j], self.vy0[j]))
            #
            self.dist1 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist1[i][j] = round(self.euclidean(self.vx1[i], self.vy1[i], self.vx1[j], self.vy1[j]))

    def euclidean(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextBTSP(n={self.n};vx0={self.vx0};vy0={self.vy0};dist0={self.dist0};vx1={self.vx1};vy1={self.vy1};dist1={self.dist1})"

# define two objective functions

def mycallback_fevaluate0(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist0[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist0[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

def mycallback_fevaluate1(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

# THIRD OBJECTIVE
def mycallback_fevaluate2(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

import random

def mycallback_constructive(problemCtx: ProblemContextBTSP) -> SolutionTSP:
    sol = SolutionTSP()
    for i in range(problemCtx.n):
        sol.cities.append(i)
    random.shuffle(sol.cities)
    sol.n = problemCtx.n
    return sol

from optframe.components import Move

class MoveSwapClass(Move):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    def __str__(self):
        return "MoveSwapClass(i="+str(self.i)+";j="+str(self.j)+")"
    def apply(self, problemCtx, sol: SolutionTSP) -> 'MoveSwapClass':
        aux = sol.cities[self.j]
        sol.cities[self.j] = sol.cities[self.i]
        sol.cities[self.i] = aux
        # must create reverse move (j,i)
        return MoveSwapClass(self.j, self.i)
    def canBeApplied(self, problemCtx, sol: SolutionTSP) -> bool:
        return True
    def eq(self, problemCtx, m2: 'MoveSwapClass') -> bool:
        return (self.i == m2.i) and (self.j == m2.j)

assert isinstance(MoveSwapClass, XMove)       # composition tests
assert MoveSwapClass in Move.__subclasses__() # classmethod style

#from optframe.components import NS

class NSSwap(object):
    @staticmethod
    def randomMove(pTSP, sol: SolutionTSP) -> MoveSwapClass:
        import random
        n = sol.n
        i = random.randint(0, n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
        # return MoveSwap(i, j)
        return MoveSwapClass(i, j)
    
#assert NSSwap in NS.__subclasses__()   # optional test

# A Crossover must combine two parent solutions and return two new ones
# Workaround: at this version, this is divided into two callbacks...

from typing import Tuple
from copy import deepcopy

def ox_cross_parts(p1, p2, k1, k2):
    # initialize offspring 's'
    s = deepcopy(p1)
    middle_p1 = p1.cities[k1:k2]
    n = len(p1.cities)
    # create offspring s with the three parts
    s.cities = [-1]*len(p1.cities[:k1]) + middle_p1 + [-1]*len(p1.cities[k2:])
    # list rest of pending elements
    rest = [x for x in p2.cities if x not in middle_p1]
    k=0
    for i in range(0, n):
      if s.cities[i] == -1:
        s.cities[i] = rest[k]
        k = k + 1
    return s

def btsp_ox_crossover(pBTSP: ProblemContextBTSP, p1: SolutionTSP, p2: SolutionTSP ) -> Tuple[SolutionTSP, SolutionTSP]:
    assert(pBTSP.n == p1.n)
    assert(p1.n == p2.n)
    assert(pBTSP.n >= 3)
    
    # select cut point
    # NOTE: randint (both sides included)
    k1 = random.randint(1, pBTSP.n - 2)
    k2 = random.randint(k1+1, pBTSP.n - 1)
    #
    s1 = ox_cross_parts(p1, p2, k1, k2)
    s2 = ox_cross_parts(p2, p1, k1, k2)
    #
    return s1, s2

# NOTE: this is just a demo... it has a problem!
# crossover pair may not be fully consistent, as each side can have a different fixed point
# This is a simple workaround for this first version

def mycallback_cross1(pBTSP: ProblemContextBTSP, p1: SolutionTSP, p2: SolutionTSP) -> SolutionTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s1

def mycallback_cross2(pBTSP: ProblemContextBTSP, p1: SolutionTSP, p2: SolutionTSP) -> SolutionTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s2
    
