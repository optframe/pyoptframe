
from optframe.core import LibArrayDouble
from typing import Tuple, Union

import ctypes

#
# decoder function: receives a problem instance and an array of random keys (as LibArrayDouble)
#

class DecoderTSP(object):
    @staticmethod
    def decodeSolution(pTSP: ProblemContextTSP, array_double : LibArrayDouble) -> SolutionTSP:
        #
        sol = SolutionTSP()
        #
        lpairs = []
        for i in range(array_double.size):
            p = [array_double.v[i], i]
            lpairs.append(p)
        #
        #print("lpairs: ", lpairs)
        sorted_list = sorted(lpairs)
        #print("sorted_list: ", sorted_list)
        #
        sol.n = pTSP.n
        sol.cities = []
        for i in range(array_double.size):
            sol.cities.append(sorted_list[i][1]) # append index of city in order
        return sol

    @staticmethod
    def decodeMinimize(pTSP: ProblemContextTSP, array_double : LibArrayDouble, needsSolution: bool) -> Tuple[Union[SolutionTSP,None], float]:
        #
        # print("decodeMinimize! needsSolution="+str(needsSolution), flush=True)
        sol = DecoderTSP.decodeSolution(pTSP, array_double)
        #
        # NOW WILL GET EVALUATION VALUE
        e = ProblemContextTSP.minimize(pTSP, sol)
        # FINALLY, WILL RETURN WHAT IS REQUIRED
        if not needsSolution:
            return (None, e)
        else:
            return (sol, e)


