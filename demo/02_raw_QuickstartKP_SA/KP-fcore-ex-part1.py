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

