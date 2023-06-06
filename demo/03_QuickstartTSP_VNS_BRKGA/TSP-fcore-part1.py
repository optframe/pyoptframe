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
    