
from optframe.components import Move

class MoveBitFlip(Move):
    def __init__(self, _k :int):
        self.k = _k
    def apply(self, problemCtx: ExampleKP, sol: SolutionKP) -> 'MoveBitFlip':
        sol.bag[self.k] = 1 - sol.bag[self.k]
        return MoveBitFlip(self.k)
    def canBeApplied(self, problemCtx: ExampleKP, sol: SolutionKP) -> bool:
        return True
    def eq(self, problemCtx: ExampleKP, m2: 'MoveBitFlip') -> bool:
        return self.k == m2.k
    