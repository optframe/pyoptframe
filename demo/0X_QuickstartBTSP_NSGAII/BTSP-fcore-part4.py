
import random

def mycallback_constructive(problemCtx: ProblemContextBTSP) -> SolutionTSP:
    sol = SolutionTSP()
    for i in range(problemCtx.n):
        sol.cities.append(i)
    random.shuffle(sol.cities)
    sol.n = problemCtx.n
    return sol
