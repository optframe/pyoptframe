
#
# decoder function: receives a problem instance and an array of random keys (as LibArrayDouble)
#
def mycallback_decoder_rk(problemCtx: ProblemContextTSP, array_double : optframe.engine.LibArrayDouble) -> SolutionTSP:
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
    sol.n = problemCtx.n
    sol.cities = []
    for i in range(array_double.size):
        sol.cities.append(sorted_list[i][1]) # append index of city in order
    return sol

