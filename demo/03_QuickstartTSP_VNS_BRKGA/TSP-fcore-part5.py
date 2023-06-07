
from optframe.components import Move

'''
# move
class MoveSwap(object):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    def __str__(self):
        return "MoveSwap(i="+str(self.i)+";j="+str(self.j)+")"
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
    

assert isinstance(MoveSwap, XMove)            # composition tests
assert not(MoveSwap in Move.__subclasses__()) # staticmethod style
'''

class MoveSwapClass(Move):
    def __init__(self, _i: int = 0, _j: int = 0):
        self.i = _i
        self.j = _j
    def __str__(self):
        return "MoveSwapClass(i="+str(self.i)+";j="+str(self.j)+")"
    def apply(self, problemCtx: ProblemContextTSP, sol: SolutionTSP) -> 'MoveSwapClass':
        aux = sol.cities[self.j]
        sol.cities[self.j] = sol.cities[self.i]
        sol.cities[self.i] = aux
        # must create reverse move (j,i)
        return MoveSwapClass(self.j, self.i)
    def canBeApplied(self, problemCtx: ProblemContextTSP, sol: SolutionTSP) -> bool:
        return True
    def eq(self, problemCtx: ProblemContextTSP, m2: 'MoveSwapClass') -> bool:
        return (self.i == m2.i) and (self.j == m2.j)


assert isinstance(MoveSwapClass, XMove)       # composition tests
assert MoveSwapClass in Move.__subclasses__() # classmethod style
