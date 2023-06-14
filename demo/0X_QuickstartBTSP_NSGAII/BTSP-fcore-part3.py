
# define two objective functions

def mycallback_fevaluate0(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist0[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist0[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

def mycallback_fevaluate1(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

# THIRD OBJECTIVE
def mycallback_fevaluate2(pBTSP: ProblemContextBTSP, s: SolutionTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f
