# continuation of ExampleKP class...
    @staticmethod
    def generateSolution(problem: 'ExampleKP') -> SolutionKP:
        import random
        sol = SolutionKP()
        sol.n = problem.n
        sol.bag = [random.randint(0, 1) for _ in range(sol.n)]
        return sol

