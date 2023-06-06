
#
# random constructive: updates parameter ptr_array_double of type (LibArrayDouble*)
#
def mycallback_constructive_rk(problemCtx: ProblemContextTSP, ptr_array_double) -> int:
    rkeys = []
    for i in range(problemCtx.n):
        key = random.random() # [0,1] uniform
        rkeys.append(key)
    #
    ptr_array_double.contents.size = len(rkeys)
    ptr_array_double.contents.v = optframe.engine.callback_adapter_list_to_vecdouble(rkeys)
    return len(rkeys)

