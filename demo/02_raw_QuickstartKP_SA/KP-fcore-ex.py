# OptFrame Python Demo 0-1 Knapsack Problem + Simulated Annealing

import optframe

class SolutionKP(object):
    def __init__(self):
        # number of items in solution
        self.n = 0
        # selected items in solution
        self.bag = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionKP(n={self.n};bag={self.bag})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo):
        sol2 = SolutionKP()
        sol2.n = self.n
        sol2.bag = [i for i in self.bag]
        return sol2

    def __del__(self):
        # print("~SolutionKP")
        pass

class ProblemContextKP(object):
    def __init__(self):
        print('Init KP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of items
        self.n = 0
        # item weights
        self.w = []
        # item profits
        self.p = []
        # knapsack capacity
        self.Q = 0.0

    def load(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            self.Q = int(lines[1])
            p_lines = lines[2].split()
            self.p = [int(i) for i in p_lines] 
            w_lines = lines[3].split()
            self.w = [int(i) for i in w_lines] 

    def __str__(self):
        return f"ProblemContextKP(n={self.n};Q={self.Q};w={self.w};p={self.p})"

import random

def mycallback_constructive(problemCtx: ProblemContextKP) -> SolutionKP:
    sol = SolutionKP()
    for i in range(0, problemCtx.n):
        sol.bag.append(random.choice([0, 1]))
    sol.n = problemCtx.n
    return sol

# remember this is an API1d method
def mycallback_fevaluate(pKP: ProblemContextKP, sol: SolutionKP):
    assert (sol.n == pKP.n)
    assert (len(sol.bag) == sol.n)
    #
    sum_w = 0.0
    sum_p = 0.0
    for i in range(0, sol.n):
        if sol.bag[i] == 1:
            sum_w += pKP.w[i]
            sum_p += pKP.p[i]
    # weight for infeasibility
    W_INF = -1000000.0
    if sum_w > pKP.Q:
        # excess is penalized
        sum_p += W_INF * (sum_w - pKP.Q)
    return sum_p

# move
class MoveBitFlip(object):
    def __init__(self):
        #print('__init__ MoveBitFlip')
        self.k = 0

    def __del__(self):
        # print("~MoveBitFlip")
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_bitflip(problemCtx: ProblemContextKP, m: MoveBitFlip, sol: SolutionKP) -> MoveBitFlip:
    k = m.k
    sol.bag[k] = 1 - sol.bag[k]
    # must create reverse move
    mv = MoveBitFlip()
    mv.k = k
    return mv

# Moves can be applied or not (best performance is to have a True here)
def cba_bitflip(problemCtx: ProblemContextKP, m: MoveBitFlip, sol: SolutionKP) -> bool:
    return True

# Move equality must be provided
def eq_bitflip(problemCtx: ProblemContextKP, m1: MoveBitFlip, m2: MoveBitFlip) -> bool:
    return m1.k == m2.k

def mycallback_ns_rand_bitflip(pKP: ProblemContextKP, sol: SolutionKP) -> MoveBitFlip:
    k = random.randint(0, pKP.n - 1)
    mv = MoveBitFlip()
    mv.k = k
    return mv
