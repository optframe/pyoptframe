
from optframe.protocols import XConstructiveRK
from optframe.core import LibArrayDouble

#
# random constructive: updates parameter ptr_array_double of type (LibArrayDouble*)
#
class RKConstructiveTSP(object):
    @staticmethod
    def generateRK(problemCtx: ProblemContextTSP, ptr_array_double : LibArrayDouble) -> int:
        rkeys = []
        for i in range(problemCtx.n):
            key = random.random() # [0,1] uniform
            rkeys.append(key)
        #
        ptr_array_double.contents.size = len(rkeys)
        ptr_array_double.contents.v = engine.callback_adapter_list_to_vecdouble(rkeys)
        return len(rkeys)

