
# A Crossover must combine two parent solutions and return two new ones
# Workaround: at this version, this is divided into two callbacks...

from typing import Tuple
from copy import deepcopy

def ox_cross_parts(p1, p2, k1, k2):
    # initialize offspring 's'
    s = deepcopy(p1)
    middle_p1 = p1.cities[k1:k2]
    n = len(p1.cities)
    # create offspring s with the three parts
    s.cities = [-1]*len(p1.cities[:k1]) + middle_p1 + [-1]*len(p1.cities[k2:])
    # list rest of pending elements
    rest = [x for x in p2.cities if x not in middle_p1]
    k=0
    for i in range(0, n):
      if s.cities[i] == -1:
        s.cities[i] = rest[k]
        k = k + 1
    return s

def btsp_ox_crossover(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP ) -> Tuple[SolutionBTSP, SolutionBTSP]:
    assert(pBTSP.n == p1.n)
    assert(p1.n == p2.n)
    assert(pBTSP.n >= 3)
    
    # select cut point
    # NOTE: randint (both sides included)
    k1 = random.randint(1, pBTSP.n - 2)
    k2 = random.randint(k1+1, pBTSP.n - 1)
    #
    s1 = ox_cross_parts(p1, p2, k1, k2)
    s2 = ox_cross_parts(p2, p1, k1, k2)
    #
    return s1, s2

# NOTE: this is just a demo... it has a problem!
# crossover pair may not be fully consistent, as each side can have a different fixed point
# This is a simple workaround for this first version

def mycallback_cross1(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s1

def mycallback_cross2(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s2
    
