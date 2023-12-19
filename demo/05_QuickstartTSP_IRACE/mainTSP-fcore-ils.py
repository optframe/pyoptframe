# OptFrame Python Demo TSP - Traveling Salesman Problem

from typing import List
import random

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

#from optframe.components import NSSeq
from optframe.components import NSIterator

# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current

class IteratorSwap(NSIterator):
    def __init__(self, _i: int, _j: int):
        self.i = _i
        self.j = _j
    def first(self, pTSP: ProblemContextTSP):
        self.i = 0
        self.j = 1
    def next(self, pTSP: ProblemContextTSP):
        if self.j < pTSP.n - 1:
            self.j = self.j+1
        else:
            self.i = self.i + 1
            self.j = self.i + 1
    def isDone(self, pTSP: ProblemContextTSP):
        return self.i >= pTSP.n - 1
    def current(self, pTSP: ProblemContextTSP):
        return MoveSwapClass(self.i, self.j)
    
assert IteratorSwap in NSIterator.__subclasses__()   # optional test
    
class NSSeqSwap(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwapClass:
        return NSSwap.randomMove(pTSP, sol)  # composition
    
    @staticmethod
    def getIterator(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
        return IteratorSwap(-1, -1)

#assert NSSeqSwap in NSSeq.__subclasses__()   # optional test
# ===========================================
# begins main() python script for TSP ILS/VNS
# ===========================================

import sys

# Adaptations for irace.
# Main() must receive params from irace.
#instancia = sys.argv[1]
instancia = "InstancesTraining/tsp-example.txt"
time = 3
localSearch = 0 # TODO
iterMax = 10
maxPert = 5
for i in range(len(sys.argv)):
    if (sys.argv[i] == "--time"):
        time = int(sys.argv[i + 1])
    if (sys.argv[i] == "-i"):
        instancia = str(sys.argv[i + 1])
    if (sys.argv[i] == "--seed"):
        random.seed(int(sys.argv[i + 1]))
    # begin CONFIG_PARAMS
    if (sys.argv[i] == "--localSearch"):
        localSearch = int(sys.argv[i + 1])
    if (sys.argv[i] == "--iterMax"):
        iterMax = int(sys.argv[i + 1])
    if (sys.argv[i] == "--maxPert"):
        maxPert = float(sys.argv[i + 1])

# import ILSLevels and BestImprovement
from optframe.heuristics import *

# loads problem from filesystem
pTSP = ProblemContextTSP()

# set SILENT
pTSP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "0")
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

# load
pTSP.load(instancia)

# Register Basic Components
comp_list = pTSP.engine.setup(pTSP)

# get index of new NS
ns_idx = pTSP.engine.add_ns_class(pTSP, NSSwap)

# get index of new NSSeq
nsseq_idx = pTSP.engine.add_nsseq_class(pTSP, NSSeqSwap)


# pack NS into a NS list
list_idx = pTSP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
# print("list_idx=", list_idx)

# print("Listing registered components:")
# pTSP.engine.list_components("OptFrame:")

# list the required parameters for OptFrame ComponentBuilder
# print("engine will list builders for OptFrame: ")
# print(pTSP.engine.list_builders("OptFrame:"))
# print()


# TODO: add IF for FirstImprovement...
bi = BestImprovement(pTSP.engine, 0, 0)
ls_idx = bi.get_id()

list_vnd_idx = pTSP.engine.create_component_list(
    "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")

vnd = VariableNeighborhoodDescent(pTSP.engine, 0, 0)
vnd_idx = vnd.get_id()


#####
#pTSP.engine.list_components("OptFrame:")

ilsl_pert = ILSLevelPertLPlus2(pTSP.engine, 0, 0)
pert_idx = ilsl_pert.get_id()

ilsl = ILSLevels(pTSP.engine, 0, 0, 1, 0, iterMax, maxPert)
lout = ilsl.search(time)
print(lout.best_e)
