
import random

def mycallback_constructive(problemCtx: ProblemContextBTSP) -> SolutionBTSP:
    sol = SolutionBTSP()
    for i in range(problemCtx.n):
        sol.cities.append(i)
    random.shuffle(sol.cities)
    sol.n = problemCtx.n
    return sol
