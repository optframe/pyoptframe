#!/usr/bin/python3

import ctypes
from ctypes import *
#
#from functools import total_ordering
from typing import TypeVar, Type
#T = TypeVar('T', bound='BigInteger')

# too many options for handling resources in python libs... trying atexit
# https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
import atexit

# perform deepcopy
# https://stackoverflow.com/questions/1500718/how-to-override-the-copy-deepcopy-operations-for-a-python-object
from copy import copy, deepcopy
import sys

# for problem
import random  # TODO: get from hf engine ?

import gc

# ==================== fcore_lib.so ===================


fcore_lib = ctypes.cdll.LoadLibrary('../build/fcore_lib.so')

FCORE_WARN_ISSUES = True

# =====================================
#   Helper Function Pointer Types
# =====================================

# py_object -> py_object
FUNC_SOL_DEEPCOPY = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object)
# py_object -> int
FUNC_UTILS_DECREF = CFUNCTYPE(
    ctypes.c_int, ctypes.py_object)
# VERYYY IMPORTANT: it seems POINTER(c_char) is writeable, where c_char_p is not...
# py_object, buffer, sz -> count
FUNC_SOL_TOSTRING = CFUNCTYPE(
    ctypes.c_size_t, ctypes.py_object, POINTER(c_char), ctypes.c_size_t)


# =====================================
#        OptFrame ADD Component
# =====================================

# problem*, solution* -> double
FUNC_FEVALUATE = CFUNCTYPE(ctypes.c_double, ctypes.py_object, ctypes.py_object)

# fcore_float64_fevaluator(void* hf, double (*_fevaluate)(void*), bool min_or_max) -> int (index)
fcore_lib.fcore_api1_add_float64_evaluator.argtypes = [
    ctypes.c_void_p, FUNC_FEVALUATE, c_bool, ctypes.py_object]
fcore_lib.fcore_api1_add_float64_evaluator.restype = ctypes.c_int32

# ----------

# problem* -> solution*
FUNC_FCONSTRUCTIVE = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object)

fcore_lib.fcore_api1_add_constructive.argtypes = [
    ctypes.c_void_p, FUNC_FCONSTRUCTIVE, ctypes.py_object,
    FUNC_SOL_DEEPCOPY, FUNC_SOL_TOSTRING, FUNC_UTILS_DECREF]
fcore_lib.fcore_api1_add_constructive.restype = ctypes.c_int32

# ----------

# problem*,solution* -> move*
FUNC_FNS_RAND = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, ctypes.py_object)

# problem*,move*,solution* -> move*
FUNC_FMOVE_APPLY = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)

# operator==: problem*,move*,move* -> bool
FUNC_FMOVE_EQ = CFUNCTYPE(
    ctypes.c_bool, ctypes.py_object, ctypes.py_object, ctypes.py_object)

# canBeApplied: problem*,move*,solution* -> bool
FUNC_FMOVE_CBA = CFUNCTYPE(
    ctypes.c_bool, ctypes.py_object, ctypes.py_object, ctypes.py_object)

# fns: hf*, func_ns, func_mv1, func_mv2, func_mv3, problem* -> int
fcore_lib.fcore_api1_add_ns.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND, FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
fcore_lib.fcore_api1_add_ns.restype = ctypes.c_int32


# ====================================
#        OptFrame GET Component
# ====================================
fcore_lib.fcore_api1_get_float64_evaluator.argtypes = [
    ctypes.c_void_p, c_int32]
fcore_lib.fcore_api1_get_float64_evaluator.restype = ctypes.c_void_p
#
fcore_lib.fcore_api1_get_constructive.argtypes = [
    ctypes.c_void_p, c_int32]
fcore_lib.fcore_api1_get_constructive.restype = ctypes.c_void_p
###


### Engine: HeuristicFactory
fcore_lib.fcore_api1_create_engine.argtypes = []
fcore_lib.fcore_api1_create_engine.restype = ctypes.c_void_p
#
fcore_lib.fcore_api1_destroy_engine.argtypes = [ctypes.c_void_p]
fcore_lib.fcore_api1_destroy_engine.restype = ctypes.c_bool
#
fcore_lib.fcore_api1_engine_test.argtypes = [ctypes.c_void_p]
fcore_lib.fcore_api1_engine_test.restype = ctypes.c_bool
#
fcore_lib.fcore_api1_engine_simulated_annealing.argtypes = [ctypes.c_void_p]
fcore_lib.fcore_api1_engine_simulated_annealing.restype = ctypes.c_bool
#
fcore_lib.fcore_api1_engine_simulated_annealing_params.argtypes = [
    ctypes.c_void_p,  ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_int, ctypes.c_double]
fcore_lib.fcore_api1_engine_simulated_annealing_params.restype = ctypes.c_bool
#
fcore_lib.fcore_api1_engine_builders.argtypes = [
    ctypes.c_void_p,  ctypes.c_char_p]
fcore_lib.fcore_api1_engine_builders.restype = ctypes.c_int
#
fcore_lib.fcore_api1_engine_check.argtypes = [
    ctypes.c_void_p]
fcore_lib.fcore_api1_engine_check.restype = ctypes.c_bool
###

#fcore_component_print(void* component);
fcore_lib.fcore_component_print.argtypes = [c_void_p]

# ======================================
#              SPECIFIC
# ======================================

# fcore_float64_fevaluator_evaluate(void* _fevaluator, bool min_or_max, void* solution_ptr) -> double
fcore_lib.fcore_api1_float64_fevaluator_evaluate.argtypes = [
    c_void_p, c_bool, ctypes.py_object]
fcore_lib.fcore_api1_float64_fevaluator_evaluate.restype = ctypes.c_double

# fcore_api1_fconstructive_gensolution(void* _fconstructive) -> py_object solution
fcore_lib.fcore_api1_fconstructive_gensolution.argtypes = [
    c_void_p]
fcore_lib.fcore_api1_fconstructive_gensolution.restype = ctypes.py_object


# =========================
#     OptFrame Engine
# =========================

class OptFrameEngine(object):
    def __init__(self):
        self.hf = fcore_lib.fcore_api1_create_engine()
        self.callback_sol_deepcopy_ptr = FUNC_SOL_DEEPCOPY(
            callback_sol_deepcopy)
        self.callback_sol_tostring_ptr = FUNC_SOL_TOSTRING(
            callback_sol_tostring)
        self.callback_utils_decref_ptr = FUNC_UTILS_DECREF(
            callback_utils_decref)
        atexit.register(self.cleanup)

    def cleanup(self):
        print("Running optframe cleanup...")
        fcore_lib.fcore_api1_destroy_engine(self.hf)

    def print_component(self, component):
        fcore_lib.fcore_component_print(component)

    def list_builders(self, pattern: str):
        if(not isinstance(pattern, str)):
            assert(False)
        b_pattern = pattern.encode('ascii')
        # type of b_pattern is 'bytes'
        #print("bytes type: ", type(b_pattern))
        return fcore_lib.fcore_api1_engine_builders(self.hf, ctypes.c_char_p(b_pattern))

    def run_sa(self):
        print("DEPRECATED")
        print("Will Begin SA")
        r = fcore_lib.fcore_api1_engine_simulated_annealing(self.hf)
        print("Finished SA")
        return r

    def run_sa_params(self, timelimit, id_ev, id_c, id_ns, alpha, iter, T):
        print("Will Begin SA Params")
        r = fcore_lib.fcore_api1_engine_simulated_annealing_params(self.hf,
                                                                   timelimit, id_ev, id_c, id_ns,
                                                                   alpha, iter, T)
        print("Finished SA Params")
        return r

    def run_test(self):
        print("Will Begin Test")
        r = fcore_lib.fcore_api1_engine_test(self.hf)
        print("Finished Test")
        return r

    def check(self, p1: int, p2: int, verbose=False) -> bool:
        return fcore_lib.fcore_api1_engine_check(self.hf, p1, p2, verbose)

    # =================== ADD =========================

    # register GeneralEvaluator (as FEvaluator) for min_callback
    def minimize(self, problemCtx, min_callback_ptr):
        #print("min_callback=", min_callback_ptr)
        idx_ev = fcore_lib.fcore_api1_add_float64_evaluator(
            # self.hf,     FUNC_FEVALUATE(min_callback), True)
            self.hf,     min_callback_ptr, True, problemCtx)
        return idx_ev

    def maximize(self, problemCtx, max_callback_ptr):
        idx_ev = fcore_lib.fcore_api1_add_float64_evaluator(
            # self.hf,     FUNC_FEVALUATE(max_callback), False)
            self.hf,     max_callback_ptr, False, problemCtx)
        return idx_ev

    def add_constructive(self, problemCtx, constructive_callback_ptr):
        #print("add_constructive begins")
        idx_c = fcore_lib.fcore_api1_add_constructive(
            #self.hf,     FUNC_FCONSTRUCTIVE(constructive_callback), problemCtx,
            self.hf,  constructive_callback_ptr, problemCtx,
            self.callback_sol_deepcopy_ptr,
            # FUNC_SOL_DEEPCOPY(callback_sol_deepcopy),
            self.callback_sol_tostring_ptr,
            # FUNC_SOL_TOSTRING(callback_sol_tostring),
            self.callback_utils_decref_ptr)
        # FUNC_UTILS_DECREF(callback_utils_decref))
        #print("add_constructive is finishing")
        return idx_c

    def add_ns(self, problemCtx, ns_rand_callback_ptr, move_apply_callback_ptr, move_eq_callback_ptr, move_cba_callback_ptr):
        #print("add_ns begins")
        idx_ns = fcore_lib.fcore_api1_add_ns(
            self.hf,  ns_rand_callback_ptr, move_apply_callback_ptr,
            move_eq_callback_ptr, move_cba_callback_ptr, problemCtx,
            self.callback_utils_decref_ptr)
        # FUNC_UTILS_DECREF(callback_utils_decref))
        #print("add_ns is finishing")
        return idx_ns

    # ===================== GET =======================

    def get_evaluator(self, idx_ev=0):
        fevaluator = fcore_lib.fcore_api1_get_float64_evaluator(
            self.hf, idx_ev)
        return fevaluator

    def get_constructive(self, idx_c=0):
        fconstructive = fcore_lib.fcore_api1_get_constructive(
            self.hf, idx_c)
        return fconstructive

    # ==================================================
    # non-standard non-api method... just for testing
    # ==================================================

    def fevaluator_evaluate(self, fevaluator_ptr: ctypes.py_object, min_or_max: bool, py_sol):
        #print("invoking 'fcore_lib.fcore_api1_float64_fevaluator_evaluate' with fevaluator_ptr=", fevaluator_ptr)
        self.print_component(fevaluator_ptr)
        pyo_view = ctypes.py_object(py_sol)
        #print("begin fevaluator_evaluate with pyo_view=", pyo_view)
        z = fcore_lib.fcore_api1_float64_fevaluator_evaluate(
            fevaluator_ptr, min_or_max, pyo_view)
        #print("'fevaluator_evaluate' final z=", z)
        return z

    def fconstructive_gensolution(self, fconstructive_ptr: ctypes.py_object) -> ctypes.py_object:
        #print("invoking 'fcore_lib.fcore_api1_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)
        self.print_component(fconstructive_ptr)
        #print("begin fconstructive_gensolution")
        pyo_sol = fcore_lib.fcore_api1_fconstructive_gensolution(
            fconstructive_ptr)
        #print("finished fconstructive_gensolution!")
        #print("pyo_sol=", pyo_sol, " count=", sys.getrefcount(pyo_sol))
        #
        # I THINK we must decref it... because it was once boxed into C++ solution and incref'ed somewhere...
        #
        cast_pyo = ctypes.py_object(pyo_sol)
        #print("cast_pyo=", cast_pyo, " count=", sys.getrefcount(cast_pyo))
        # ERROR: when decref, it segfaults... don't know why
        # ctypes.pythonapi.Py_DecRef(cast_pyo)
        return cast_pyo.value

# ==============================


def callback_utils_incref(pyo: ctypes.py_object):
    print("callback_utils_incref: ", sys.getrefcount(pyo), " will get +1")
    ctypes.pythonapi.Py_IncRef(pyo)
    return sys.getrefcount(pyo)


def callback_utils_decref(pyo):
    if(isinstance(pyo, ctypes.py_object)):
        #print("WARNING DECREF: IS ctypes.py_object")
        pyo = pyo.value
        #print("pyo:", pyo)
    #print("callback_utils_decref: ", sys.getrefcount(pyo), " will get -1")
    # IMPORTANT: 'pyo' may come as a Real Python Object, not a 'ctypes.py_object'
    cast_pyo = ctypes.py_object(pyo)
    ctypes.pythonapi.Py_DecRef(cast_pyo)
    x = sys.getrefcount(pyo)
    #print("x=", x, "force delete object = ", pyo)
    # if x <= 4:
    #    print("x=", x, "strange object = ", pyo)
    #del pyo
    #    print(gc.is_finalized(pyo))
    return x

# ==============================

# =========================
#       Solution KP
# =========================


count_solkp = 0
count_plus_solkp = 0
count_minus_solkp = 0
#
count_solkp_new_copy = 0
count_solkp_new_deepcopy = 0
#
count_move_bitflip = 0
count_plus_move_bitflip = 0
count_minus_move_bitflip = 0


class ExampleSol(object):

    def __init__(self):
        #print('__init__ ExampleSol')
        self.n = 0
        self.bag = []
        global count_solkp
        global count_plus_solkp
        count_solkp = count_solkp+1
        count_plus_solkp = count_plus_solkp+1

    def __str__(self):
        return f"ExampleSol(n={self.n};bag={self.bag})"

    def __copy__(self):
        assert(False)
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        global count_solkp_new_copy
        count_solkp_new_copy = count_solkp_new_copy + 1
        return result

    # def __deepcopy__(self, memo):
    #    cls = self.__class__
    #    result = cls.__new__(cls)
    #    result.n = self.n
    #    result.bag = deepcopy(self.bag)
        #
        #global count_solkp_new_deepcopy
        #count_solkp_new_deepcopy = count_solkp_new_deepcopy + 1
        #
        return result
        #
        assert(False)
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for n, bag in self.__dict__.items():
            setattr(result, n, deepcopy(bag, memo))
        global count_solkp_new_deepcopy
        count_solkp_new_deepcopy = count_solkp_new_deepcopy + 1
        return result

    def __del__(self):
        # print("~ExampleSol")
        global count_solkp
        global count_minus_solkp
        count_solkp = count_solkp-1
        count_minus_solkp = count_minus_solkp-1
        pass


class ESolutionKP(object):
    def __init__(self):
        #print('__init__ ESolutionKP...')
        # ExampleSol
        self.first = None
        self.second = 0.0


def callback_sol_tostring(sol: ExampleSol, pt: ctypes.c_char_p, ptsize: ctypes.c_size_t):
    mystr = sol.__str__()  # + '\0'
    mystr_bytes = mystr.encode()  # str.encode(mystr)
    pa = cast(pt, POINTER(c_char * ptsize))
    pa.contents.value = mystr_bytes

    return len(mystr)


def callback_sol_deepcopy(sol: ExampleSol):
    #print("invoking 'callback_sol_deepcopy'... sol=", sol)
    if(isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert(False)
        # if FCORE_WARN_ISSUES == True:
        print("WARNING: IS ctypes.py_object")
        sol = sol.value
    #
    #sol2 = deepcopy(sol)
    #
    sol2 = ExampleSol()
    sol2.n = sol.n
    sol2.bag = [i for i in sol.bag]
    #
    #pyo = ctypes.py_object(sol2)
    # ctypes.pythonapi.Py_IncRef(pyo)  # TODO: do we need this? I hope so...
    #print("final sol=", sol2)
    return sol2

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
    # print("count=", sys.getrefcount(sol)) # count=2
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
        global count_move_bitflip
        global count_plus_move_bitflip
        count_move_bitflip = count_move_bitflip+1
        count_plus_move_bitflip = count_plus_move_bitflip+1

    def __del__(self):
        # print("~MoveBitFlip")
        global count_move_bitflip
        global count_minus_move_bitflip
        count_move_bitflip = count_move_bitflip-1
        count_minus_move_bitflip = count_minus_move_bitflip-1
        pass


# C++: uptr<Move<XES>> (*fRandom)(const XES&);


# TODO: 'sol: ExampleSol' should become 'esol: ESolutionKP'.. but lib must receive both sol and evaluation (as double, or double ptr... TODO think)
def mycallback_ns_rand_bitflip(pKP: ExampleKP, sol: ExampleSol) -> MoveBitFlip:
    k = random.randint(0, pKP.n-1)
    mv = MoveBitFlip()
    mv.k = k
    # TODO: should we IncRef this? probably...
    return mv


# ===============================

#    FMove(
#     const M& _m,
#     M (*_fApply)(const M&, XES&),                                                // fApply
#     bool (*_fCanBeApplied)(const M&, const XES&) = fDefaultCanBeApplied<M, XES>, // fCanBeApplied
#     bool (*_fCompareEq)(const M&, const Move<XES>&) = fDefaultCompareEq<M, XES>  // fCompareEq
#     )

# TODO: 'sol: ExampleSol' should become 'esol: ESolutionKP'.. but lib must receive both sol and evaluation (as double, or double ptr... TODO think)
def mycallback_move_apply_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> MoveBitFlip:
    if(isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert(False)
        if FCORE_WARN_ISSUES == True:
            print("WARNING3: IS ctypes.py_object")
        sol = sol.value
    k = m.k
    #esol.first.bag[k] = 1 - esol.first.bag[k]
    sol.bag[k] = 1 - sol.bag[k]
    # must create reverse move
    mv = MoveBitFlip()
    mv.k = k
    # TODO: should we IncRef this? probably...
    return mv

# TODO: 'sol: ExampleSol' should become 'esol: ESolutionKP'.. but lib must receive both sol and evaluation (as double, or double ptr... TODO think)


def mycallback_move_cba_bitflip(problemCtx: ExampleKP, m: MoveBitFlip, sol: ExampleSol) -> bool:
    return True


def mycallback_move_eq_bitflip(problemCtx: ExampleKP, m1: MoveBitFlip, m2: MoveBitFlip) -> bool:
    return m1.k == m2.k


def test_leak_new_solution(engine, problemCtx: ExampleKP) -> ExampleSol:
    fc = engine.get_constructive(0)
    engine.print_component(fc)
    solxx = engine.fconstructive_gensolution(fc)
    print("solxx=", solxx)
    return True


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
fev = engine.get_evaluator()
engine.print_component(fev)
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
#z = engine.fevaluator_evaluate(fev, True, sol)
#
print("")
print("==========================")
print("manually generate solution")
print("==========================")

s = mycallback_constructive(pKP)
print("")
print("count=", sys.getrefcount(s))
print(s)

print("")

c_idx = engine.add_constructive(pKP, call_c)
print("c_idx=", c_idx)


fc = engine.get_constructive(c_idx)
engine.print_component(fc)
print("")
print("========================")
print("engine generate solution")
print("========================")
#
solxx = engine.fconstructive_gensolution(fc)
print("")
print("count=", sys.getrefcount(solxx))
print("solxx:", solxx)
#
print("")
print("============================")
print("engine test evaluate (again)")
print("============================")
z1 = engine.fevaluator_evaluate(fev, False, solxx)
print("evaluation:", z1)


print("")
print("=====================")
print("engine add ns bitflip")
print("=====================")

call_ns_bitflip = FUNC_FNS_RAND(mycallback_ns_rand_bitflip)
call_move_apply = FUNC_FMOVE_APPLY(mycallback_move_apply_bitflip)
call_move_eq = FUNC_FMOVE_EQ(mycallback_move_eq_bitflip)
call_move_cba = FUNC_FMOVE_CBA(mycallback_move_cba_bitflip)

# get index of new NS
ns_idx = engine.add_ns(pKP, call_ns_bitflip,
                       call_move_apply, call_move_eq, call_move_cba)
print("ns_idx=", ns_idx)

print("")
print("============================")
print("    stress test generate    ")
print("============================")
will_stress = False
if will_stress:
    while True:
        sol_inf = engine.fconstructive_gensolution(fc)
        print("sol_inf:", sol_inf)
        z1 = engine.fevaluator_evaluate(fev, False, sol_inf)
        print("evaluation:", z1)
else:
    print("OK. no stress...")

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

# engine.run_sa()
#
engine.run_sa_params(5.0, ev_idx, c_idx, ns_idx, 0.98, 200, 9999999)
# engine.run_sa(alpha, T, ...)
# engine.run_brkga()

# engine.run_test() # run generic test on C++... just for debugging

# must keep callback variables alive until the end... for now
print(call_fev)
print(call_c)
print(call_ns_bitflip)
print(call_move_apply)
print(call_move_eq)
print(call_move_cba)


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
exit(0)
