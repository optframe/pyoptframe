# remember this is an API1d method
def mycallback_fevaluate(pKP: ProblemContextKP, sol: SolutionKP):
    assert (sol.n == pKP.n)
    assert (len(sol.bag) == sol.n)
    #
    sum_w = 0.0
    sum_p = 0.0
    for i in range(0, sol.n):
        if sol.bag[i] == 1:
            sum_w += pKP.w[i]
            sum_p += pKP.p[i]
    # weight for infeasibility
    W_INF = -1000000.0
    if sum_w > pKP.Q:
        # excess is penalized
        sum_p += W_INF * (sum_w - pKP.Q)
    return sum_p
