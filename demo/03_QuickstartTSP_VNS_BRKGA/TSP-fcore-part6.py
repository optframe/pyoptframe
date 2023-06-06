
class NSSeqBitFlip(object):
    @staticmethod
    def randomMove(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
        import random
        i = random.randint(0, pTSP.n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, pTSP.n - 1)
            j = random.randint(0, pTSP.n - 1)
        return MoveSwap(i, j)