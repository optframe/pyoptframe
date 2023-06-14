# OptFrame Python Demo TSP - Traveling Salesman Problem

from typing import List
import random

# DO NOT REORDER 'import sys ...'
# ****** REMOVE THIS BLOCK IF YOU HAVE INSTALLED OPTFRAME LIBRARY ******
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
# **********************************************************************
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

# import ILSLevels and BestImprovement
from optframe.heuristics import *

# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')
print(pTSP)

# Register Basic Components
comp_list = pTSP.engine.setup(pTSP)
print(comp_list)

# get index of new NS
ns_idx = pTSP.engine.add_ns_class(pTSP, NSSwap)
print("ns_idx=", ns_idx)

# get index of new NSSeq
nsseq_idx = pTSP.engine.add_nsseq_class(pTSP, NSSeqSwap)
print("nsseq_idx=", nsseq_idx)

# ========= play a little bit =========

gev_idx = comp_list[0] # GeneralEvaluator
ev_idx  = comp_list[1] # Evaluator
print("evaluator id:", ev_idx)

c_idx = comp_list[2]
print("c_idx=", c_idx)

is_idx = IdInitialSearch(0)
print("is_idx=", is_idx)

# test each component

fev = pTSP.engine.get_evaluator(ev_idx)
pTSP.engine.print_component(fev)

fc = pTSP.engine.get_constructive(c_idx)
pTSP.engine.print_component(fc)

solxx = pTSP.engine.fconstructive_gensolution(fc)
print("test solution:", solxx)

z1 = pTSP.engine.fevaluator_evaluate(fev, True, solxx)
print("test evaluation:", z1)

# some basic tests with moves and iterator
move = MoveSwapClass(0,1) # swap 0 with 1
print("move=",move)
m1 = NSSwap.randomMove(pTSP, solxx)
print(m1)

print("begin test with iterator")
it = NSSeqSwap.getIterator(pTSP, solxx)
it.first(pTSP)
while not it.isDone(pTSP):
    m = it.current(pTSP)
    print(m)
    it.next(pTSP)
print("end test with iterator")

# ======== end playing ========

# pack NS into a NS list
list_idx = pTSP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)

# print("Listing registered components:")
# pTSP.engine.list_components("OptFrame:")

# list the required parameters for OptFrame ComponentBuilder
# print("engine will list builders for OptFrame: ")
# print(pTSP.engine.list_builders("OptFrame:"))
# print()

# make next local search component silent (loglevel 0)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

print("building 'BI' neighborhood exploration as local search", flush=True)
bi = BestImprovement(pTSP.engine, 0, 0)
ls_idx = bi.get_id()
print("ls_idx=", ls_idx, flush=True)

print("creating local search list", flush=True)
list_vnd_idx = pTSP.engine.create_component_list(
    "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")
print("list_vnd_idx=", list_vnd_idx)


print("building 'VND' local search")
vnd = VariableNeighborhoodDescent(pTSP.engine, 0, 0)
vnd_idx = vnd.get_id()
print("vnd_idx=", vnd_idx)


#####
#pTSP.engine.list_components("OptFrame:")

ilsl_pert = ILSLevelPertLPlus2(pTSP.engine, 0, 0)
pert_idx = ilsl_pert.get_id()
print("pert_idx=", pert_idx)

# pTSP.engine.list_components("OptFrame:")

# make next global search component info (loglevel 3)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "3")

# build Iterated Local Search (ILS) Levels with iterMax=10 maxPert=5
ilsl = ILSLevels(pTSP.engine, 0, 0, 1, 0, 10, 5)
print("will start ILS for 3 seconds")
lout = ilsl.search(3.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)

print("FINISHED")
