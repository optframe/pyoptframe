# OptFrame Python Demo 0-1 Knapsack Problem + Simulated Annealing

from typing import List

# DO NOT REORDER 'import sys ...'
# ****** REMOVE THIS BLOCK IF YOU HAVE INSTALLED OPTFRAME LIBRARY ******
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
# **********************************************************************

from optframe import *
from optframe.protocols import *

class SolutionKP(object):
    def __init__(self):
        self.n   : int = 0        # number of items in solution
        self.bag : List[int] = [] # selected items in solution
    def __str__(self):
        return f"SolutionKP(n={self.n};bag={self.bag})"
    


class ExampleKP(object):
    def __init__(self):
        self.engine = Engine()
        self.n : int = 0          # number of items
        self.w : List[float] = [] # item weights
        self.p : List[float] = [] # item profits
        self.Q : float = 0.0      # knapsack capacity

    def load(self, filename : str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            self.Q = int(lines[1])
            p_lines = lines[2].split()
            self.p = [int(i) for i in p_lines] 
            w_lines = lines[3].split()
            self.w = [int(i) for i in w_lines] 

    def __str__(self):
        return f"ExampleKP(n={self.n};Q={self.Q};w={self.w};p={self.p})"

# continuation of ExampleKP class...
    @staticmethod
    def generateSolution(problem: 'ExampleKP') -> SolutionKP:
        import random
        sol = SolutionKP()
        sol.n = problem.n
        sol.bag = [random.randint(0, 1) for _ in range(sol.n)]
        return sol

# continuation of ExampleKP class...
    @staticmethod
    def maximize(pKP: 'ExampleKP', sol: SolutionKP) -> float:
        import numpy as np
        wsum = np.dot(sol.bag, pKP.w)
        if wsum > pKP.Q:
            return -1000.0*(wsum - pKP.Q)
        return np.dot(sol.bag, pKP.p)

# optional tests...
assert isinstance(SolutionKP, XSolution)     # composition tests 
assert isinstance(ExampleKP,  XProblem)      # composition tests 
assert isinstance(ExampleKP,  XConstructive) # composition tests    
assert isinstance(ExampleKP,  XMaximize)     # composition tests

from optframe.components import Move

class MoveBitFlip(Move):
    def __init__(self, _k :int):
        self.k = _k
    def apply(self, problemCtx: ExampleKP, sol: SolutionKP) -> 'MoveBitFlip':
        sol.bag[self.k] = 1 - sol.bag[self.k]
        return MoveBitFlip(self.k)
    def canBeApplied(self, problemCtx: ExampleKP, sol: SolutionKP) -> bool:
        return True
    def eq(self, problemCtx: ExampleKP, m2: 'MoveBitFlip') -> bool:
        return self.k == m2.k
    
class NSBitFlip(object):
    @staticmethod
    def randomMove(pKP: ExampleKP, sol: SolutionKP) -> MoveBitFlip:
        import random
        return MoveBitFlip(random.randint(0, pKP.n - 1))

assert isinstance(NSBitFlip, XNS)     # composition tests

# ===========================
# begins main() python script
# ===========================

# get SimulatedAnnealing
from optframe.core import LogLevel
from optframe.heuristics import *

# set random seed for system
# random.seed(10)

# loads problem from filesystem
pKP = ExampleKP()
pKP.load('knapsack-example.txt')
#pKP.n = 5
#pKP.w = [1, 2, 3, 7, 8]
#pKP.p = [1, 1, 1, 5, 5]
#pKP.Q = 10.0



# register model components (evaluation function, constructive, ...)
pKP.engine.setup(pKP)
ev_idx = 0
c_idx = 0
is_idx = 0
# is_idx = pKP.engine.create_initial_search(ev_idx, c_idx)

# register NS class
pKP.engine.add_ns_class(pKP, NSBitFlip) 
ns_idx = 0

# make engine disabled (loglevel 4)
pKP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", str(LogLevel.Disabled))

# ======= play a little bit ========

fev = pKP.engine.get_evaluator(ev_idx)
pKP.engine.print_component(fev)

fc = pKP.engine.get_constructive(c_idx)
pKP.engine.print_component(fc)

solxx = pKP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z1 = pKP.engine.fevaluator_evaluate(fev, False, solxx)
print("evaluation:", z1)

# ====== end playing ======

# list the required parameters for OptFrame SA ComponentBuilder
print("engine will list builders for :BasicSA ")
nbuilders=pKP.engine.list_builders(":BasicSA")
print("nbuilders =", nbuilders)

# pack NS into a NS list
list_idx = pKP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")

# make global search silent (loglevel 0)
pKP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

# check components!
print("will invoke check module")
b=pKP.engine.check(100, 10, False)
assert(b)

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
sa = BasicSimulatedAnnealing(pKP.engine, 0, 0, list_idx, 0.98, 100, 99999)
print("will invoke Simulated Annealing")
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)

# =========================
# ends main() python script
# =========================
