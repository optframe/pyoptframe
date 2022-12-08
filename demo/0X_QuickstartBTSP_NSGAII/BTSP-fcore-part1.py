# OptFrame Python Demo BTSP - Bi-objective Traveling Salesman Problem

import os

# DO NOT REORDER 'import sys ...'
import sys
str_path=os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, str_path)

# THIS PACKAGE IS LOCAL (../optframe), NOT FROM PACKAGE MANAGER...
# GOOD FOR LOCAL TESTING!

# DO NOT REORDER 'from optframe.engine ...'
from optframe.engine import Engine

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