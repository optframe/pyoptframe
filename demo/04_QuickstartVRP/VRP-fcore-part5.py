

# move
class MoveVRPExchange(object):
    def __init__(self):
        self.r = 0
        self.c1 = 0
        self.c2 = 0

    def __del__(self):
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_vrp_exchange(pVRP: ProblemContextVRP, m: MoveVRPExchange, sol: SolutionVRP) -> MoveVRPExchange:
    r = m.r
    c1 = m.c1
    c2 = m.c2
    #
    aux = sol.cities[j]
    sol.cities[j] = sol.cities[i]
    sol.cities[i] = aux
    # must create reverse move (j,i)
    mv = MoveSwap()
    mv.i = j
    mv.j = i
    return mv

# Moves can be applied or not (best performance is to have a True here)
def cba_vrp_exchange(pVRP: ProblemContextVRP, m: MoveVRPExchange, sol: SolutionVRP) -> bool:
    rep = getRoutes(sol);  # se.first.getR();
    bool all_positive = (c1 >= 0) && (c2 >= 0) && (r >= 0);
    return all_positive && (rep.at(r).size() >= 2);
    return True

# Move equality must be provided
def eq_vrp_exchange(problemCtx: ProblemContextTSP, m1: MoveSwap, m2: MoveSwap) -> bool:
    return (m1.i == m2.i) and (m1.j == m2.j)
