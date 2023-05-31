# OptFrame Python Demo 0-1 Knapsack Problem + Simulated Annealing

import os
from typing import List
from optframe import *

class SolutionKP(object):
    def __init__(self):
        self.n   : int = 0        # number of items in solution
        self.bag : List[int] = [] # selected items in solution
    def __str__(self):
        return f"SolutionKP(n={self.n};bag={self.bag})"
    
