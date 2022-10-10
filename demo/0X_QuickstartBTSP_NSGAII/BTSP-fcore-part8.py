
# A Crossover must combine two parent solutions and return two new ones
# Workaround: at this version, this is divided into two callbacks...

from typing import Tuple
from copy import deepcopy

def btsp_point_crossover(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP ) -> Tuple[SolutionBTSP, SolutionBTSP]:
    assert(pBTSP.n == p1.n)
    assert(p1.n == p2.n)
    
    # select cut point
    k = random.randint(0, pBTSP.n - 2) + 1
    #
    s1 = deepcopy(p1)
    s2 = deepcopy(p2)
    #
    for i in range(k):
      s1.cities[i] = p1.cities[i];
      s2.cities[i] = p2.cities[i];
    for j in range(k, pBTSP.n):
      s1.cities[j] = p2.cities[j];
      s2.cities[j] = p1.cities[j];
    #
    # TODO: we need to fix this crossover, so that cities wont repeat!
    # TODO: replace here by OX crossover?
    #
    print("WARNING: we need to fix this crossover, otherwise cities may repeat!")

    return s1, s2

# NOTE: this is just a demo... it has a problem!
# crossover pair may not be fully consistent, as each side can have a different fixed point
# This is a simple workaround for this first version

def mycallback_cross1(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_point_crossover(pBTSP, p1, p2)
    return s1

def mycallback_cross2(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_point_crossover(pBTSP, p1, p2)
    return s2
    
