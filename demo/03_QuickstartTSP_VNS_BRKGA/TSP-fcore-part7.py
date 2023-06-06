
# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current
#class NSSeqBitFlip(object):
    class IteratorSwap(object):
        def __init__(self, _i: int, _j: int):
            self.i = _i
            self.j = _j
#class NSSeqBitFlip(object):
    @staticmethod
    def getIterator(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
        return IteratorSwap(-1, -1)
    @staticmethod
    def first(pTSP: ProblemContextTSP, it: IteratorSwap):
        it.i = 0
        it.j = 1
    @staticmethod
    def next(pTSP: ProblemContextTSP, it: IteratorSwap):
        if it.j < pTSP.n - 1:
            it.j = it.j+1
        else:
            it.i = it.i + 1
            it.j = it.i + 1
    @staticmethod
    def isDone(pTSP: ProblemContextTSP, it: IteratorSwap):
        return it.i >= pTSP.n - 1

    @staticmethod
    def current(pTSP: ProblemContextTSP, it: IteratorSwap):
        return MoveSwap(it.i, it.j)
