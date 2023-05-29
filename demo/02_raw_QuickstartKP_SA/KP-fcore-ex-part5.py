
# move
class MoveBitFlip(object):
    def __init__(self):
        #print('__init__ MoveBitFlip')
        self.k = 0

    def __del__(self):
        # print("~MoveBitFlip")
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_bitflip(problemCtx: ProblemContextKP, m: MoveBitFlip, sol: SolutionKP) -> MoveBitFlip:
    k = m.k
    sol.bag[k] = 1 - sol.bag[k]
    # must create reverse move
    mv = MoveBitFlip()
    mv.k = k
    return mv

# Moves can be applied or not (best performance is to have a True here)
def cba_bitflip(problemCtx: ProblemContextKP, m: MoveBitFlip, sol: SolutionKP) -> bool:
    return True

# Move equality must be provided
def eq_bitflip(problemCtx: ProblemContextKP, m1: MoveBitFlip, m2: MoveBitFlip) -> bool:
    return m1.k == m2.k

