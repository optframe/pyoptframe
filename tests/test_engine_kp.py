#!/usr/bin/python3

# for problem
import random  # TODO: get from hf engine ?


from optframe.engine import OptFrameEngine
# helpers
#from optframe.engine import callback_sol_deepcopy
from optframe.engine import *  # FUNC_FEVALUATE, FUNC_FCONSTRUCTIVE, FUNC_FNS_RAND


# =========================
#       Solution KP
# =========================

class ExampleSol(object):

    def __init__(self):
        self.n = 0
        self.bag = []

    def __str__(self):
        return f"ExampleSol(n={self.n};bag={self.bag})"

    def __copy__(self):
        assert(False)

    def __deepcopy__(self, memo):
        sol2 = ExampleSol()
        sol2.n = self.n
        sol2.bag = [i for i in self.bag]
        return sol2

    def __del__(self):
        # print("~ExampleSol")
        pass


# =========================
#       Problem KP
# =========================


class ExampleKP(object):
    # def __init__(self, param=0):
    #    self.p = param
    def __init__(self):
        print('Init KP')
        # number of items
        self.n = 0
        # item weights
        self.w = []
        # item profits
        self.p = []
        # knapsack capacity
        self.Q = 0.0

    def __str__(self):
        return f"ExampleKP(n={self.n};Q={self.Q};w={self.w};p={self.p})"


def mycallback_fevaluate(pKP: ExampleKP, sol: ExampleSol):
    #print("python: invoking 'mycallback_fevaluate' with problem and solution sol=", sol)
    if(isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert(False)
        if FCORE_WARN_ISSUES == True:
            print("WARNING2: IS ctypes.py_object")
        sol = sol.value
    assert(sol.n == pKP.n)
    assert(len(sol.bag) == sol.n)
    #
    sum_w = 0.0
    sum_p = 0.0
    for i in range(0, sol.n):
        if sol.bag[i] == 1:
            sum_w += pKP.w[i]
            sum_p += pKP.p[i]
    # weight for infeasibility
    W_INF = -1000.0
    if sum_w > pKP.Q:
        # excess is penalized
        #print("will penalize: Q=", pKP.Q, "sum_w=", sum_w)
        sum_p += W_INF * (sum_w-pKP.Q)
    #print("result is: ", sum_p)
    return sum_p


def mycallback_constructive(problemCtx: ExampleKP) -> ExampleSol:
    #print("\tinvoking mycallback_constructive for problem: ", problemCtx)
    sol = ExampleSol()
    for i in range(0, problemCtx.n):
        sol.bag.append(random.choice([0, 1]))
    sol.n = problemCtx.n
    #print("\tfinished mycallback_constructive with sol: ", sol)
    return sol


# ========================================================
# IMPORTANT: MoveBitFlip represents a move here,
# while on C++ it only represents a Move Structure...
# It will work fine, anyway. What pleases the user most ;)
# ========================================================
class MoveBitFlip(object):
    def __init__(self):
        #print('__init__ MoveBitFlip')
        self.k = 0

    def __del__(self):
        # print("~MoveBitFlip")
        pass


# C++: uptr<Move<XES>> (*fRandom)(const XES&);


# TODO: 'sol: ExampleSol' should become 'esol: ESolutionKP'.. but lib must receive both sol and evaluation (as double, or double ptr... TODO think)
def mycallback_ns_rand_bitflip(pKP: ExampleKP, sol: ExampleSol) -> MoveBitFlip:
    k = random.randint(0, pKP.n-1)
    mv = MoveBitFlip()
    mv.k = k
    return mv

# TODO: 'sol: ExampleSol' should become 'esol: ESolutionKP'.. but lib must receive both sol and evaluation (as double, or double ptr... TODO think)


def mycallback_move_apply_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> MoveBitFlip:
    k = m.k
    sol.bag[k] = 1 - sol.bag[k]
    # must create reverse move
    mv = MoveBitFlip()
    mv.k = k
    return mv


def mycallback_move_cba_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> bool:
    return True


def mycallback_move_eq_bitflip(problemCtx: ExampleKP, m1: MoveBitFlip, m2: MoveBitFlip) -> bool:
    return m1.k == m2.k


class IteratorBitFlip(object):
    def __init__(self):
        # print('__init__ IteratorBitFlip')
        self.k = 0

    def __del__(self):
        # print("__del__ IteratorBitFlip")
        pass


def mycallback_nsseq_it_init_bitflip(pKP: ExampleKP, sol: ExampleSol) -> IteratorBitFlip:
    it = IteratorBitFlip()
    it.k = 0
    return it


def mycallback_nsseq_it_first_bitflip(pKP: ExampleKP, it: IteratorBitFlip):
    it.k = 0


def mycallback_nsseq_it_next_bitflip(pKP: ExampleKP, it: IteratorBitFlip):
    it.k = it.k+1


def mycallback_nsseq_it_isdone_bitflip(pKP: ExampleKP, it: IteratorBitFlip):
    return it.k >= pKP.n


def mycallback_nsseq_it_current_bitflip(pKP: ExampleKP, it: IteratorBitFlip):
    mv = MoveBitFlip()
    mv.k = it.k
    return mv


# =============================
#       BEGIN SCRIPT
# =============================
print("=========================")
print("BEGIN with OptFrameEngine")
print("=========================")
print("")
print("Create Callbacks KP object")
print("")
call_fev = FUNC_FEVALUATE(mycallback_fevaluate)
call_c = FUNC_FCONSTRUCTIVE(mycallback_constructive)
print("call_fev=", call_fev)
print("call_c=", call_c)

engine = OptFrameEngine()
print("call_ev:", call_fev)
print("call_c:", call_c)
pKP = ExampleKP()
pKP.n = 5
pKP.w = [1, 2, 3, 4, 5]
pKP.p = [5, 4, 3, 2, 1]
pKP.Q = 6.0
print(pKP)

ev_idx = engine.maximize(pKP, call_fev)
print("evaluator id:", ev_idx)

c_idx = engine.add_constructive(pKP, call_c)
print("c_idx=", c_idx)

is_idx = engine.create_initial_search(ev_idx, c_idx)
print("is_idx=", is_idx)


call_ns_bitflip = FUNC_FNS_RAND(mycallback_ns_rand_bitflip)
call_move_apply = FUNC_FMOVE_APPLY(mycallback_move_apply_bitflip)
call_move_eq = FUNC_FMOVE_EQ(mycallback_move_eq_bitflip)
call_move_cba = FUNC_FMOVE_CBA(mycallback_move_cba_bitflip)

# get index of new NS
ns_idx = engine.add_ns(pKP, call_ns_bitflip,
                       call_move_apply, call_move_eq, call_move_cba)
print("ns_idx=", ns_idx)

list_idx = engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)


call_nsseq_it_init_bitflip = FUNC_FNSSEQ_IT_INIT(
    mycallback_nsseq_it_init_bitflip)
call_nsseq_it_first_bitflip = FUNC_FNSSEQ_IT_FIRST(
    mycallback_nsseq_it_first_bitflip)
call_nsseq_it_next_bitflip = FUNC_FNSSEQ_IT_NEXT(
    mycallback_nsseq_it_next_bitflip)
call_nsseq_it_isdone_bitflip = FUNC_FNSSEQ_IT_ISDONE(
    mycallback_nsseq_it_isdone_bitflip)
call_nsseq_it_current_bitflip = FUNC_FNSSEQ_IT_CURRENT(
    mycallback_nsseq_it_current_bitflip)

# get index of new NSSeq
nsseq_idx = engine.add_nsseq(pKP,
                             call_ns_bitflip,
                             call_nsseq_it_init_bitflip,
                             call_nsseq_it_first_bitflip,
                             call_nsseq_it_next_bitflip,
                             call_nsseq_it_isdone_bitflip,
                             call_nsseq_it_current_bitflip,
                             call_move_apply, call_move_eq, call_move_cba)
print("nsseq_idx=", nsseq_idx)

# ============= CHECK =============
print("")
print("Engine: will check")
print("")
engine.check(100, 10, False)
print("pass...")

print()
print("engine will list builders ")
print(engine.list_builders("OptFrame:"))
print()
print("engine will list builders for :BasicSA ")
print(engine.list_builders(":BasicSA"))
print()


print("")
print("testing builder (build_single_obj_search) for SA...")
print("")

sos_idx = engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:SA:BasicSA",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.99 100 999")
print("sos_idx=", sos_idx)

print("")
print("testing execution of SingleObjSearch (run_sos_search) for SA...")
print("")

lout = engine.run_sos_search(sos_idx, 4.0)
print('lout=', lout)

print("")
print("testing builder (build_local_search) for BI...")
print("")

ls_idx = engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:FI",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS:NSFind:NSSeq 0")
print("ls_idx=", ls_idx)

engine.list_components("OptFrame:")

print("")
print("testing builder (build_component) for ILSLevels...")
print("")

pert_idx = engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")
print("pert_idx=", pert_idx)

engine.list_components("OptFrame:")


print("")
print("testing builder (build_single_obj_search) for ILS...")
print("")

sos_idx = engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 0 OptFrame:ILS:LevelPert 0  50  3")
print("sos_idx=", sos_idx)

print("")
print("testing execution of SingleObjSearch (run_sos_search) for ILS...")
print("")

lout = engine.run_sos_search(sos_idx, 4.5)
print('lout=', lout)

# must keep callback variables alive until the end... for now
print(call_fev)
print(call_c)
print(call_ns_bitflip)
print(call_move_apply)
print(call_move_eq)
print(call_move_cba)

print(call_nsseq_it_init_bitflip)
print(call_nsseq_it_first_bitflip)
print(call_nsseq_it_next_bitflip)
print(call_nsseq_it_isdone_bitflip)
print(call_nsseq_it_current_bitflip)
