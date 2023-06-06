# OptFrame Python Demo TSP - Traveling Salesman Problem

import os
from typing import List
import random
# DO NOT REORDER 'import sys ...'
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
#
from optframe import *

class SolutionTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n : int = 0
        # visited cities as a list
        self.cities : List[int] = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionTSP(n={self.n};cities={self.cities})"
    
class ProblemContextTSP(object):
    def __init__(self):
        # float engine for OptFrame
        self.engine = Engine(APILevel.API1d)
        # number of cities
        self.n = 0
        # x coordinates
        self.vx = []
        # y coordinates
        self.vy = []
        # distance matrix
        self.dist = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename: str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx.append(int(id_x_y[1]))
               self.vy.append(int(id_x_y[2]))
            #
            self.dist = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist[i][j] = round(self.euclidean(self.vx[i], self.vy[i], self.vx[j], self.vy[j]))

    def euclidean(self, x1, y1, x2, y2):
        import math
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextTSP(n={self.n};vx={self.vx};vy={self.vy};dist={self.dist})"
# continuation of ProblemContextTSP class...
    @staticmethod
    def minimize(pTSP: 'ProblemContextTSP', s: SolutionTSP) -> float:
        assert (s.n == pTSP.n)
        assert (len(s.cities) == s.n)
        # remember this is an API1d method
        f = 0.0
        for i in range(pTSP.n-1):
          f += pTSP.dist[s.cities[i]][s.cities[i + 1]];
        f += pTSP.dist[s.cities[int(pTSP.n) - 1]][s.cities[0]];
        return f
# continuation of ProblemContextTSP class...
    @staticmethod
    def generateSolution(problemCtx: 'ProblemContextTSP') -> SolutionTSP:
        sol = SolutionTSP()
        for i in range(problemCtx.n):
            sol.cities.append(i)
        random.shuffle(sol.cities)
        sol.n = problemCtx.n
        return sol

# optional tests...
assert isinstance(SolutionTSP, XSolution)            # composition tests 
assert isinstance(ProblemContextTSP,  XProblem)      # composition tests 
assert isinstance(ProblemContextTSP,  XConstructive) # composition tests    
assert isinstance(ProblemContextTSP,  XMinimize)     # composition tests


# move
class MoveSwap(object):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    def __str__(self):
        return "MoveSwap(i="+str(self.i)+";j="+str(self.j)+")"
    @staticmethod
    def apply(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> 'MoveSwap':
        aux = sol.cities[m.j]
        sol.cities[m.j] = sol.cities[m.i]
        sol.cities[m.i] = aux
        # must create reverse move (j,i)
        return MoveSwap(m.j, m.i)
    @staticmethod
    def canBeApplied(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> bool:
        return True
    @staticmethod
    def eq(problemCtx: ProblemContextTSP, m1: 'MoveSwap', m2: 'MoveSwap') -> bool:
        return (m1.i == m2.i) and (m1.j == m2.j)

class NSSwap(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
        import random
        i = random.randint(0, pTSP.n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, pTSP.n - 1)
            j = random.randint(0, pTSP.n - 1)
        return MoveSwap(i, j)
# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current

class IteratorSwap(object):
    def __init__(self, _i: int, _j: int):
        self.i = _i
        self.j = _j
    @staticmethod
    def first(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        it.i = 0
        it.j = 1
    @staticmethod
    def next(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        if it.j < pTSP.n - 1:
            it.j = it.j+1
        else:
            it.i = it.i + 1
            it.j = it.i + 1
    @staticmethod
    def isDone(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        return it.i >= pTSP.n - 1

    @staticmethod
    def current(pTSP: ProblemContextTSP, it: 'IteratorSwap'):
        return MoveSwap(it.i, it.j)
    
class NSSeqSwap(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
        return NSSwap.randomMove(pTSP, sol) # reuse method from NSSwap
    
    @staticmethod
    def getIterator(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
        return IteratorSwap(-1, -1)
