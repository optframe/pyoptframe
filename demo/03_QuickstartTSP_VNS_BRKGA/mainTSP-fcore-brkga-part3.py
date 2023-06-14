
from optframe.core import LibArrayDouble

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

