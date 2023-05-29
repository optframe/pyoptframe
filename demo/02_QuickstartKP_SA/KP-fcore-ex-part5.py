
class MoveBitFlip(object):
    def __init__(self, _k :int):
        self.k = _k
    @staticmethod
    def apply(problemCtx: ExampleKP, m: 'MoveBitFlip', sol: SolutionKP) -> 'MoveBitFlip':
        sol.bag[m.k] = 1 - sol.bag[m.k]
        return MoveBitFlip(m.k)
    @staticmethod
    def canBeApplied(problemCtx: ExampleKP, m: 'MoveBitFlip', sol: SolutionKP) -> bool:
        return True
    @staticmethod
    def eq(problemCtx: ExampleKP, m1: 'MoveBitFlip', m2: 'MoveBitFlip') -> bool:
        return m1.k == m2.k
    