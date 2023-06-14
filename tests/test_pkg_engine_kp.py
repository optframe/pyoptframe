#!/usr/bin/python3

import random  # TODO: get from hf engine ?

#from optframe.engine import OptFrameEngine
import optframe

# ==========================================
# THIS IS AN EXAMPLE OF THE KNAPSACK PROBLEM
# ==========================================

# =========================
#       Solution KP
# =========================

# this is the definition of a single solution on the knapsack problem


class ExampleSol(object):

    def __init__(self):
        # number of items in solution
        self.n = 0
        # selected items in solution
        self.bag = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"ExampleSol(n={self.n};bag={self.bag})"

    # MUST provide some deepcopy mechanism
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

# this is the definition of a Knapsack Problem instance

class ExampleKP(object):

    def __init__(self):
        print('Init KP')
        # may store current optframe engine for local usage
        self.engine = None
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


# Definition of an evaluation function
# MUST receive two inputs: Problem and Solution
# MUST return a double representing the evaluation value of this solution

def mycallback_fevaluate(pKP: ExampleKP, sol: ExampleSol):
    assert (sol.n == pKP.n)
    assert (len(sol.bag) == sol.n)
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
        sum_p += W_INF * (sum_w - pKP.Q)
    #print("result is: ", sum_p)
    return sum_p

# Definition of a constructive method
# MUST receive one input: Problem
# MUST return a valid Solution for this Problem (it CAN be Infeasible)


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

# Definition of a Neighborhood Structure and Move
# There are four types of Neighborhood Structures in OptFrame: NS, NSFind, NSSeq and NSEnum
# A Move MUST receive perform three actions: Apply, Equality and CanBeApplied
# A NS MUST return a Random Move for the given neighborhood

class MoveBitFlip(object):
    def __init__(self):
        #print('__init__ MoveBitFlip')
        self.k = 0

    def __del__(self):
        # print("~MoveBitFlip")
        pass

# Generating a Random Move


def mycallback_ns_rand_bitflip(pKP: ExampleKP, sol: ExampleSol) -> MoveBitFlip:
    k = random.randint(0, pKP.n - 1)
    mv = MoveBitFlip()
    mv.k = k
    return mv

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)


def mycallback_move_apply_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> MoveBitFlip:
    k = m.k
    sol.bag[k] = 1 - sol.bag[k]
    # must create reverse move
    mv = MoveBitFlip()
    mv.k = k
    return mv

# Moves can be applied or not (best performance is to have a True here)


def mycallback_move_cba_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> bool:
    return True


# Move equality must be provided

def mycallback_move_eq_bitflip(problemCtx: ExampleKP, m1: MoveBitFlip, m2: MoveBitFlip) -> bool:
    return m1.k == m2.k

# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current


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
    it.k = it.k + 1


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


# creates a Toy problem with 5 items
pKP = ExampleKP()
pKP.n = 5
pKP.w = [1, 2, 3, 4, 5]
pKP.p = [5, 4, 3, 2, 1]
pKP.Q = 6.0
# initializes optframe engine
pKP.engine = optframe.engine.Engine(optframe.engine.APILevel.API1d)
print(pKP)

ev_idx = pKP.engine.maximize(pKP, mycallback_fevaluate)
print("evaluator id:", ev_idx)

c_idx = pKP.engine.add_constructive(pKP, mycallback_constructive)
print("c_idx=", c_idx)

is_idx = pKP.engine.create_initial_search(ev_idx, c_idx)
print("is_idx=", is_idx)


# get index of new NS
ns_idx = pKP.engine.add_ns(pKP,
                           mycallback_ns_rand_bitflip,
                           mycallback_move_apply_bitflip,
                           mycallback_move_eq_bitflip,
                           mycallback_move_cba_bitflip)
print("ns_idx=", ns_idx)

list_idx = pKP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)


# get index of new NSSeq
nsseq_idx = pKP.engine.add_nsseq(pKP,
                                 mycallback_ns_rand_bitflip,
                                 mycallback_nsseq_it_init_bitflip,
                                 mycallback_nsseq_it_first_bitflip,
                                 mycallback_nsseq_it_next_bitflip,
                                 mycallback_nsseq_it_isdone_bitflip,
                                 mycallback_nsseq_it_current_bitflip,
                                 mycallback_move_apply_bitflip,
                                 mycallback_move_eq_bitflip,
                                 mycallback_move_cba_bitflip)
print("nsseq_idx=", nsseq_idx)

# ============= CHECK =============
print("")
print("Engine: will check")
print("")
pKP.engine.check(100, 10, False)
print("pass...")

print()
print("engine will list builders ")
print(pKP.engine.list_builders("OptFrame:"))
print()
print("engine will list builders for :BasicSA ")
print(pKP.engine.list_builders(":BasicSA"))
print()


print("")
print("testing builder (build_global_search) for SA...")
print("")

gs_idx = pKP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.99 100 999")
print("sos_idx=", gs_idx)

print("")
print("testing execution of GlobalSearch (run_global_search) for SA...")
print("")

lout = pKP.engine.run_global_search(gs_idx, 4.0)
print('lout=', lout)

print("")
print("testing builder (build_local_search) for BI...")
print("")

ls_idx = pKP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:FI",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS:NSFind:NSSeq 0")
print("ls_idx=", ls_idx)

pKP.engine.list_components("OptFrame:")

print("")
print("testing builder (build_component) for ILSLevels...")
print("")

pert_idx = pKP.engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")
print("pert_idx=", pert_idx)

pKP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_single_obj_search) for ILS...")
print("")

sos_idx = pKP.engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 0 OptFrame:ILS:LevelPert 0  50  3")
print("sos_idx=", sos_idx)

print("")
print("testing execution of SingleObjSearch (run_sos_search) for ILS...")
print("")

lout = pKP.engine.run_sos_search(sos_idx, 4.5)
print('lout=', lout)

print("FINISHED!")
