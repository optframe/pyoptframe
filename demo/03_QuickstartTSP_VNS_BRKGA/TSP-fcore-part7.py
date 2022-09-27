
# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current


class IteratorSwap(object):
    def __init__(self):
        # print('__init__ IteratorSwap')
        self.k = 0

    def __del__(self):
        # print("__del__ IteratorSwap")
        pass


def mycallback_nsseq_it_init_swap(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
    it = IteratorSwap()
    it.i = -1
    it.j = -1
    return it


def mycallback_nsseq_it_first_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    it.i = 0
    it.j = 1


def mycallback_nsseq_it_next_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    if it.j < pTSP.n - 1:
        it.j = it.j+1
    else:
        it.i = it.i + 1
        it.j = it.i + 1

def mycallback_nsseq_it_isdone_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    return it.i >= pTSP.n - 1


def mycallback_nsseq_it_current_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    mv = MoveSwap()
    mv.i = it.i
    mv.j = it.j
    return mv
