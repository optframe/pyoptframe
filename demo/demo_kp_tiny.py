#!/usr/bin/python3

import os
import random
import numpy as np
from typing import List

# DO NOT REORDER 'import sys ...'
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
#
#import optframe
from optframe import Engine
from optframe.components import NSIterator
from optframe.protocols import XProblem, XSolution, XMaximize, XConstructive, XMove, XNS, XNSIterator, XNSSeq
from optframe.engine import LibArrayDouble, callback_adapter_list_to_vecdouble
from optframe import APILevel, LogLevel, SearchStatus

class ExampleSol(object):
    def __init__(self):
        self.n : int = 0
        self.bag : List[int] = []
    def __str__(self):
        return f"ExampleSol(n={self.n};bag={self.bag})"

class ExampleKP(object):
    def __init__(self):
        self.engine = Engine()
        self.n : int = 0          # number of items
        self.w : List[float] = [] # item weights
        self.p : List[float] = [] # item profits
        self.Q : float = 0.0      # knapsack capacity
    def __str__(self):
        return f"ExampleKP(n={self.n};Q={self.Q};w={self.w};p={self.p})"
    # random constructive
    @staticmethod
    def generateSolution(problem: 'ExampleKP') -> ExampleSol:
        sol = ExampleSol()
        sol.n = problem.n
        sol.bag = [random.randint(0, 1) for _ in range(sol.n)]
        return sol
    @staticmethod
    def maximize(pKP: 'ExampleKP', sol: ExampleSol) -> float:
        wsum = np.dot(sol.bag, pKP.w)
        if wsum > pKP.Q:
            return -1000.0*(wsum - pKP.Q)
        return np.dot(sol.bag, pKP.p)

assert isinstance(ExampleSol, XSolution)    # composition tests 
assert isinstance(ExampleKP, XProblem)      # composition tests 
assert isinstance(ExampleKP, XConstructive) # composition tests    
assert isinstance(ExampleKP, XMaximize)     # composition tests

class MoveBitFlip(object):
    def __init__(self, _k :int):
        self.k = _k
    @staticmethod
    def apply(problemCtx: ExampleKP, m: 'MoveBitFlip', sol: ExampleSol) -> 'MoveBitFlip':
        sol.bag[m.k] = 1 - sol.bag[m.k]
        return MoveBitFlip(m.k)
    @staticmethod
    def canBeApplied(problemCtx: ExampleKP, m: 'MoveBitFlip', sol: ExampleSol) -> bool:
        return True
    @staticmethod
    def eq(problemCtx: ExampleKP, m1: 'MoveBitFlip', m2: 'MoveBitFlip') -> bool:
        return m1.k == m2.k

class NSBitFlip(object):
    @staticmethod
    def randomMove(pKP: ExampleKP, sol: ExampleSol) -> MoveBitFlip:
        return MoveBitFlip(random.randint(0, pKP.n - 1))

assert isinstance(MoveBitFlip, XMove) # composition tests
assert isinstance(NSBitFlip, XNS)     # composition tests

class IteratorBitFlip(NSIterator):
    def __init__(self, _k:int):
        self.k = _k
    def first(self, p: ExampleKP):
        self.k = 0
    def next(self, p: ExampleKP):
        self.k = self.k + 1
    def isDone(self, p: ExampleKP) -> bool:
        return self.k >= p.n
    def current(self, p: ExampleKP):
        return MoveBitFlip(self.k)

class NSSeqBitFlip(object):
    @staticmethod
    def randomMove(pKP: ExampleKP, sol: ExampleSol) -> MoveBitFlip:
        return NSBitFlip.randomMove(pKP, sol)
    @staticmethod
    def getIterator(pKP: ExampleKP, sol: ExampleSol) -> IteratorBitFlip:
        return IteratorBitFlip(0)

assert isinstance(IteratorBitFlip, XNSIterator) # composition tests
assert isinstance(NSSeqBitFlip, XNSSeq) # composition tests


# ----------------------

# LibArrayDouble
def mycallback_constructive_rk(problemCtx: ExampleKP, ptr_array_double: LibArrayDouble) -> int:
    #
    rkeys : List[float] = []
    for _ in range(problemCtx.n):
        key = random.random() # [0,1] uniform
        rkeys.append(key)
    
    #print(" python 'mycallback_constructive_rk': generated keys (in python): ", rkeys)
    # set output array
    ptr_array_double.contents.size = len(rkeys)
    ptr_array_double.contents.v = callback_adapter_list_to_vecdouble(rkeys)

    # ======= PRINT CONTENTS OF ARRAY v =======
    #for i in range(ptr_array_double.contents.size):
    #    print("i=",i," -> ",ptr_array_double.contents.v[i])
    # =========================================

    return len(rkeys)

def mycallback_decoder_rk(problemCtx: ExampleKP, array_double : LibArrayDouble) -> ExampleSol:
    #
    #print("begin decoder with array=",array_double)
    #print("begin decoder with array=",array_double.size)
    #print("begin decoder with array=",array_double.v)
    # FOR TSP!!! NOT KP...
    #lpairs = []
    #for i in range(array_double.size):
    #    p = [array_double.v[i], i]
    #    lpairs.append(p)
    #print("lpairs: ", lpairs)
    #sorted_list = sorted(lpairs)
    #print("sorted_list: ", sorted_list)
    
    sol = ExampleSol()
    for i in range(0, problemCtx.n):
        if array_double.v[i] <= 0.5:
            sol.bag.append(0)
        else:
            sol.bag.append(1)
    sol.n = problemCtx.n
    return sol

KP_EXAMPLE_SILENT = True
# =============================
#       BEGIN SCRIPT
# =============================
if not KP_EXAMPLE_SILENT:
    print("=========================")
    print("BEGIN with OptFrameEngine")
    print("=========================")

#
pKP = ExampleKP()
pKP.n = 5
pKP.w = [1, 2, 3, 4, 5]
pKP.p = [5, 4, 3, 2, 1]
pKP.Q = 6.0
#
if not KP_EXAMPLE_SILENT:
    pKP.engine = Engine(APILevel.API1d, LogLevel.Debug)
else:
    pKP.engine = Engine(APILevel.API1d, LogLevel.Silent)

if not KP_EXAMPLE_SILENT:
    print(pKP)

##################

print("==-Experimental-==")
json_out = pKP.engine.experimental_get_parameter("")
print("json_out=",json_out)
pKP.engine.experimental_set_parameter("NS_VALID_RANDOM_MOVE_MAX_TRIES", "2")
json_out = pKP.engine.experimental_get_parameter("")
print("json_out=",json_out)

##################

#ev_idx = pKP.engine.maximize(pKP, mycallback_fevaluate)
ev_idx = pKP.engine.add_maximize_class(pKP, ExampleKP)
#
if not KP_EXAMPLE_SILENT:
    print("evaluator id:", ev_idx)
    print("Listing components:")
    pKP.engine.list_components("OptFrame:")

fev = pKP.engine.get_evaluator()

if not KP_EXAMPLE_SILENT:
    pKP.engine.print_component(fev)
#
# print("")
# print("=====================")
#print("create empty solution")
# print("=====================")
#sol = ExampleSol()
# print(sol)
# print("")
# print("====================")
#print("engine test evaluate")
# print("====================")
#z = pKP.engine.fevaluator_evaluate(fev, True, sol)
#
if not KP_EXAMPLE_SILENT:
    print("")
    print("==========================")
    print("manually generate solution")
    print("==========================")

s = ExampleKP.generateSolution(pKP)

if not KP_EXAMPLE_SILENT:
    print("")
    print("count=", sys.getrefcount(s))
    print(s)

    print("")

#c_idx = pKP.engine.add_constructive(pKP, mycallback_constructive)
c_idx = pKP.engine.add_constructive_class(pKP, ExampleKP)


if not KP_EXAMPLE_SILENT:
    print("c_idx=", c_idx)

is_idx = pKP.engine.create_initial_search(ev_idx, c_idx)

#if not KP_EXAMPLE_SILENT:
print("is_idx=", is_idx)

fc = pKP.engine.get_constructive(c_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.print_component(fc)
    print("")
    print("========================")
    print("engine generate solution")
    print("========================")
#

solxx = pKP.engine.fconstructive_gensolution(fc)


if not KP_EXAMPLE_SILENT:
    print("")
    print("count=", sys.getrefcount(solxx))
    print("solxx:", solxx)

    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(fc)
    #
    print("")
    print("============================")
    print("engine test evaluate (again)")
    print("============================")

z1 = pKP.engine.fevaluator_evaluate(fev, False, solxx)

if not KP_EXAMPLE_SILENT:
    print("evaluation:", z1)

    print("")
    print("=====================")
    print("engine add ns bitflip")
    print("=====================")

# get index of new NS
#ns_idx = pKP.engine.add_ns(pKP, mycallback_ns_rand_bitflip,
#                           mycallback_move_apply_bitflip, mycallback_move_eq_bitflip, mycallback_move_cba_bitflip)
ns_idx = pKP.engine.add_ns_class(pKP, NSBitFlip)
if not KP_EXAMPLE_SILENT:
    print("ns_idx=", ns_idx)


list_idx = pKP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")



if not KP_EXAMPLE_SILENT:
    print("list_idx=", list_idx)

if not KP_EXAMPLE_SILENT:
    print("")
    print("========================")
    print("engine add nsseq bitflip")
    print("========================")



# get index of new NSSeq
#nsseq_idx = pKP.engine.add_nsseq(pKP,
#                                 mycallback_ns_rand_bitflip,
#                                 mycallback_nsseq_it_init_bitflip,
#                                 mycallback_nsseq_it_first_bitflip,
#                                 mycallback_nsseq_it_next_bitflip,
#                                 mycallback_nsseq_it_isdone_bitflip,
#                                 mycallback_nsseq_it_current_bitflip,
#                                 mycallback_move_apply_bitflip, mycallback_move_eq_bitflip, mycallback_move_cba_bitflip)
nsseq_idx = pKP.engine.add_nsseq_class(pKP, NSSeqBitFlip)

if not KP_EXAMPLE_SILENT:
    print("nsseq_idx=", nsseq_idx)


if not KP_EXAMPLE_SILENT:
    print("")
    print("============================")
    print("    stress test generate    ")
    print("============================")
    will_stress = False
    if will_stress:
        while True:
            sol_inf = pKP.engine.fconstructive_gensolution(fc)
            print("sol_inf:", sol_inf)
            z1 = pKP.engine.fevaluator_evaluate(fev, False, sol_inf)
            print("evaluation:", z1)
    else:
        print("OK. no stress...")

# ============= CHECK =============

if not KP_EXAMPLE_SILENT:
    print("")
    print("Engine: will check")
    print("")

# LogLevel::Info(3) for check module
pKP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "3")

pKP.engine.check(100, 10, False)

if not KP_EXAMPLE_SILENT:
    print("pass...")

if True:
    print()
    print("engine will list builders ")
    print("count=", pKP.engine.list_builders("OptFrame:"))
    print()
    print("engine will list builders for :BasicSA ")
    print("count=", pKP.engine.list_builders(":BasicSA"))
    print()
    print("engine will list builders for :BasicTabuSearch ")
    print("count=", pKP.engine.list_builders(":BasicTabuSearch"))
    print()

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing handmade SA (run_sa_params) on C++...")
    print("")
    # DISABLED
    if False:
        pKP.engine.run_sa_params(5.0, ev_idx, c_idx, ns_idx, 0.98, 200, 9999999)
    #

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_global_search) for SA...")
    print("")


g_idx = pKP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.99 100 999")

if not KP_EXAMPLE_SILENT:
    print("g_idx=", g_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing execution of GlobalSearch (run_global_search) for SA...")
    print("")

lout = pKP.engine.run_global_search(g_idx, 4.0)

if not KP_EXAMPLE_SILENT:
    print('lout=', lout)

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_local_search) for BI...")
    print("")

ls_idx = pKP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:FI",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS:NSFind:NSSeq 0")

if not KP_EXAMPLE_SILENT:
    print("ls_idx=", ls_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_component) for ILSLevels...")
    print("")

pert_idx = pKP.engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")

if not KP_EXAMPLE_SILENT:
    print("pert_idx=", pert_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")


###########

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_single_obj_search) for ILS...")
    print("")

sos_idx = pKP.engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 0 OptFrame:ILS:LevelPert 0  50  3")

if not KP_EXAMPLE_SILENT:
    print("sos_idx=", sos_idx)

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing execution of SingleObjSearch (run_sos_search) for ILS...")
    print("")

# r = pKP.engine.component_set_loglevel(
#    "OptFrame:GlobalSearch:SingleObjSearch "+str(sos_idx), 4, False)
#print("r=", r)
# r = pKP.engine.component_set_loglevel(
#    "OptFrame:LocalSearch "+str(0), 4, False)
#print("r=", r)

lout = pKP.engine.run_sos_search(sos_idx, 4.5)

print('SA output =', lout)
ss = SearchStatus(lout.status)
print('SA status =', ss)

###########

c_rk_idx = pKP.engine.add_constructive_rk(pKP, mycallback_constructive_rk)

if not KP_EXAMPLE_SILENT:
    print("c_rk_idx=", c_rk_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")

initepop_rk_id = pKP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicInitialEPopulationRKBuilder", 
    "OptFrame:Constructive:EA:RK:ConstructiveRK 0",
    "OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK")

if not KP_EXAMPLE_SILENT:
    print("initepop_rk_id=", initepop_rk_id)

if not KP_EXAMPLE_SILENT:
    print("")
    print("WILL CREATE DECODER!!")

dec_rk_idx = pKP.engine.add_decoder_rk(pKP, mycallback_decoder_rk)

if not KP_EXAMPLE_SILENT:
    print("dec_rk_idx=", dec_rk_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")

if not KP_EXAMPLE_SILENT:
    print("")
    print("WILL BUILD COMPLETE DECODER WITH EVALUATOR!!")

drk_rk_id = pKP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicDecoderRandomKeysBuilder", 
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:EA:RK:DecoderRandomKeysNoEvaluation 0",
    "OptFrame:EA:RK:DecoderRandomKeys")

if not KP_EXAMPLE_SILENT:
    print("drk_rk_id=", drk_rk_id)

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_global_search) for BRKGA...")
    print("")

g_idx = pKP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:EA:RK:BRKGA",
    "OptFrame:EA:RK:DecoderRandomKeys 0  OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK 0 "
    "30 100 0.2 0.4 0.6")

if not KP_EXAMPLE_SILENT:
    print("g_idx=", g_idx)

if not KP_EXAMPLE_SILENT:
    pKP.engine.list_components("OptFrame:")

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing execution of GlobalSearch (run_global_search) for BRKGA...")
    print("")

lout = pKP.engine.run_global_search(g_idx, 4.9)

print('BRKGA output =', lout)
#


###########################
#       Tabu Search
###########################

if not KP_EXAMPLE_SILENT:
    print("")
    print("testing builder (build_global_search) for Tabu Search...")
    print("")

# make it silent
pKP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

g_idx = pKP.engine.build_global_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:TS:BasicTabuSearch",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0 "
    "OptFrame:NS:NSFind:NSSeq 0 "
    "1 10")

if not KP_EXAMPLE_SILENT:
    print("g_idx=", g_idx)

lout = pKP.engine.run_global_search(g_idx, 4.7)

print('BasicTabuSearch output =', lout)

##################

if not KP_EXAMPLE_SILENT:
    print("")
    print("count_solkp=", count_solkp)
    print("count_plus_solkp=", count_plus_solkp)
    print("count_minus_solkp=", count_minus_solkp)
    print("count_solkp_new_copy=", count_solkp_new_copy)
    print("count_solkp_new_deepcopy=", count_solkp_new_deepcopy)
    print("")
    print("count_move_bitflip=", count_move_bitflip)
    print("count_plus_move_bitflip=", count_plus_move_bitflip)
    print("count_minus_move_bitflip=", count_minus_move_bitflip)
    print("")
    print("count_it_bitflip=", count_it_bitflip)
    print("")
