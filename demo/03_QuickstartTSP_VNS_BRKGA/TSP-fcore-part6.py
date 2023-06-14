
#from optframe.components import NS

class NSSwap(object):
    @staticmethod
    def randomMove(pTSP, sol: SolutionTSP) -> MoveSwapClass:
        import random
        n = sol.n
        i = random.randint(0, n - 1)
        j = i
        while  j <= i:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
        # return MoveSwap(i, j)
        return MoveSwapClass(i, j)
    
#assert NSSwap in NS.__subclasses__()   # optional test
