

# move
class MoveSwap(object):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    @staticmethod
    def apply(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> 'MoveSwap':
        aux = sol.cities[m.j]
        sol.cities[m.j] = sol.cities[m.i]
        sol.cities[m.i] = aux
        # must create reverse move (j,i)
        return MoveSwap(m.j, m.i)
    @staticmethod
    def canBeApplied(problemCtx: ProblemContextTSP, m: 'MoveSwap', sol: SolutionTSP) -> bool:
        return True
    @staticmethod
    def eq(problemCtx: ProblemContextTSP, m1: 'MoveSwap', m2: 'MoveSwap') -> bool:
        return (m1.i == m2.i) and (m1.j == m2.j)
