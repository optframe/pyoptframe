# OptFrame Python Demo 0-1 Knapsack Problem + Simulated Annealing

from typing import List

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
