import random

def mycallback_constructive(problemCtx: ProblemContextKP) -> SolutionKP:
    sol = SolutionKP()
    for i in range(0, problemCtx.n):
        sol.bag.append(random.choice([0, 1]))
    sol.n = problemCtx.n
    return sol

