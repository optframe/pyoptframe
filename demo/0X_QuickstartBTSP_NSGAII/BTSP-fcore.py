# OptFrame Python Demo BTSP - Bi-objective Traveling Salesman Problem

import os

# DO NOT REORDER 'import sys ...'
#import sys
#str_path=os.path.abspath(
#    os.path.join(os.path.dirname(__file__), '../../'))
#sys.path.insert(0, str_path)

# THIS PACKAGE IS LOCAL (../optframe), NOT FROM PACKAGE MANAGER...
# GOOD FOR LOCAL TESTING!

# DO NOT REORDER 'from optframe.engine ...'
#from optframe.engine import Engine

# DO NOT REORDER 'import sys ...'
# ****** REMOVE THIS BLOCK IF YOU HAVE INSTALLED OPTFRAME LIBRARY ******
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
# **********************************************************************

import optframe

class SolutionBTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n = 0
        # visited cities as a list
        self.cities = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionBTSP(n={self.n};cities={self.cities})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo):
        sol2 = SolutionBTSP()
        sol2.n = self.n
        sol2.cities = [i for i in self.cities]
        return sol2

    def __del__(self):
        # print("~SolutionBTSP")
        pass
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

def mycallback_fevaluate0(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist0[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist0[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

def mycallback_fevaluate1(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

# THIRD OBJECTIVE
def mycallback_fevaluate2(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

import random

def mycallback_constructive(problemCtx: ProblemContextBTSP) -> SolutionBTSP:
    sol = SolutionBTSP()
    for i in range(problemCtx.n):
        sol.cities.append(i)
    random.shuffle(sol.cities)
    sol.n = problemCtx.n
    return sol


# move
class MoveSwap(object):
    def __init__(self):
        #print('__init__ MoveSwap')
        self.i = 0
        self.j = 0

    def __del__(self):
        # print("~MoveSwap")
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_swap(problemCtx: ProblemContextBTSP, m: MoveSwap, sol: SolutionBTSP) -> MoveSwap:
    i = m.i
    j = m.j
    #
    aux = sol.cities[j]
    sol.cities[j] = sol.cities[i]
    sol.cities[i] = aux
    # must create reverse move (j,i)
    mv = MoveSwap()
    mv.i = j
    mv.j = i
    return mv

# Moves can be applied or not (best performance is to have a True here)
def cba_swap(problemCtx: ProblemContextBTSP, m: MoveSwap, sol: SolutionBTSP) -> bool:
    return True

# Move equality must be provided
def eq_swap(problemCtx: ProblemContextBTSP, m1: MoveSwap, m2: MoveSwap) -> bool:
    return (m1.i == m2.i) and (m1.j == m2.j)

def mycallback_ns_rand_swap(pBTSP: ProblemContextBTSP, sol: SolutionBTSP) -> MoveSwap:
    i = random.randint(0, pBTSP.n - 1)
    j = i
    while  j<= i:
        i = random.randint(0, pBTSP.n - 1)
        j = random.randint(0, pBTSP.n - 1)
    mv = MoveSwap()
    mv.i = i
    mv.j = j
    return mv


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

def btsp_ox_crossover(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP ) -> Tuple[SolutionBTSP, SolutionBTSP]:
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

def mycallback_cross1(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s1

def mycallback_cross2(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s2
    
