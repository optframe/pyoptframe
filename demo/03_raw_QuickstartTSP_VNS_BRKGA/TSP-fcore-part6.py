
def mycallback_ns_rand_swap(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
    i = random.randint(0, pTSP.n - 1)
    j = i
    while  j<= i:
        i = random.randint(0, pTSP.n - 1)
        j = random.randint(0, pTSP.n - 1)
    mv = MoveSwap()
    mv.i = i
    mv.j = j
    return mv

