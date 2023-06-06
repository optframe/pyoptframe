# OptFrame Python Demo TSP - Traveling Salesman Problem

import optframe

class SolutionTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n = 0
        # visited cities as a list
        self.cities = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionTSP(n={self.n};cities={self.cities})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo):
        sol2 = SolutionTSP()
        sol2.n = self.n
        sol2.cities = [i for i in self.cities]
        return sol2

    def __del__(self):
        # print("~SolutionTSP")
        pass