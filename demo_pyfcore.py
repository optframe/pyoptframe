#!/usr/bin/python3

import ctypes
from ctypes import *
from secrets import randbelow
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

# ==================== fcore_lib.so ===================


fcore_lib = ctypes.cdll.LoadLibrary('build/fcore_lib.so')
fcore_lib.fcore_test_print_1.argtypes = [
    # ctypes.c_void_p, ctypes.c_int]
    ctypes.py_object, ctypes.c_int]
fcore_lib.fcore_test_print_1.restype = ctypes.c_bool

FUNC_TEST = CFUNCTYPE(c_int, ctypes.py_object)  # py_object -> int

############

FUNC_SOL_DEEPCOPY = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object)  # py_object -> py_object
FUNC_UTILS_DECREF = CFUNCTYPE(
    ctypes.c_int, ctypes.py_object)  # py_object -> int
# VERYYY IMPORTANT: it seems POINTER(c_char) is writeable, where c_char_p is not...
FUNC_SOL_TOSTRING = CFUNCTYPE(
    ctypes.c_size_t, ctypes.py_object, POINTER(c_char), ctypes.c_size_t)  # py_object, buffer, sz -> count

fcore_lib.fcore_test_gensolution.argtypes = [ctypes.py_object]
fcore_lib.fcore_test_gensolution.restype = ctypes.c_void_p

fcore_lib.fcore_test_invokesolution.argtypes = [ctypes.c_void_p, FUNC_TEST]
fcore_lib.fcore_test_invokesolution.restype = ctypes.c_void_p


# function evaluate(int[] v, int sz) -> int (evaluation)
FUNC_EVALUATE = CFUNCTYPE(c_int, POINTER(c_int), c_int)
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.py_object))
#
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.c_void_p))
#
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.py_object))
# FUNC_TEST = CFUNCTYPE(c_int, ctypes.py_object)  # py_object -> int
fcore_lib.fcore_test_func.argtypes = [
    # ctypes.c_void_p, FUNC_TEST, ctypes.c_int]
    ctypes.py_object, FUNC_TEST, ctypes.c_int]
fcore_lib.fcore_test_func.restype = ctypes.c_bool

# ======================================
#                ADD
# =====================================

# fcore_float64_fevaluator(double (*_fevaluate)(void*), bool min_or_max) -> void*
FUNC_FEVALUATE = CFUNCTYPE(c_double, ctypes.py_object)

fcore_lib.fcore_api1_add_float64_evaluator.argtypes = [
    ctypes.c_void_p, FUNC_FEVALUATE, c_bool]
fcore_lib.fcore_api1_add_float64_evaluator.restype = ctypes.c_int32

FUNC_FCONSTRUCTIVE = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object)  # problem* -> solution*

fcore_lib.fcore_api1_add_constructive.argtypes = [
    ctypes.c_void_p, FUNC_FCONSTRUCTIVE, ctypes.py_object,
    FUNC_SOL_DEEPCOPY, FUNC_SOL_TOSTRING, FUNC_UTILS_DECREF]
fcore_lib.fcore_api1_add_constructive.restype = ctypes.c_int32

# ====================================
#                GET
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
fcore_lib.fcore_api1_destroy_engine.argtypes = [ctypes.c_void_p]
fcore_lib.fcore_api1_destroy_engine.restype = ctypes.c_bool
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

# ======================================


# ===============
# VERY GOOD EXAMPLE IN PYTHON
# https://stackoverflow.com/questions/52053434/how-to-cast-a-ctypes-pointer-to-an-instance-of-a-python-class#52055019
#
# ===================

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

# class FCore(object):


class ExampleSol(object):
    # def __init__(self, param=0):
    #    self.p = param
    def __init__(self):
        print('__init__ ExampleSol. Creating empty solution...')
        self.n = 0
        self.bag = []

    def __str__(self):
        return f"ExampleSol(n={self.n};bag={self.bag})"

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for n, bag in self.__dict__.items():
            setattr(result, n, deepcopy(bag, memo))
        return result

    def foo(self):
        return 30  # self.p

# https://stackoverflow.com/questions/69724210/python-ctypes-how-to-write-string-to-given-buffer
#


def callback_sol_tostring(sol: ExampleSol, pt: ctypes.c_char_p, ptsize: ctypes.c_size_t):
    mystr = sol.__str__()  # + '\0'
    mystr_bytes = mystr.encode()  # str.encode(mystr)
    pa = cast(pt, POINTER(c_char * ptsize))
    pa.contents.value = mystr_bytes

    return len(mystr)

# def callback_sol_deepcopy(sol: ExampleSol):
#    pyo = ctypes.py_object(sol)


def callback_sol_deepcopy(sol: ExampleSol):
    sol2 = deepcopy(sol)
    pyo = ctypes.py_object(sol2)
    ctypes.pythonapi.Py_IncRef(pyo)  # TODO: do we need this? I hope so...
    return pyo

# ===================


def mycallback(userData: ExampleSol):
    print("mycallback from Python: {:s}".format(mycallback.__name__))
    print("will get type of object!")
    print(type(userData))

    return userData.foo()


def callback_fevaluate(userData: ExampleSol):
    print("EVALUATE From Python: {:s}".format(mycallback.__name__))
    v = 0.5
    print("test value is: ", v)
    return v


def callback_constructive(problemCtx: ExampleKP) -> ExampleSol:
    print("\tinvoking callback_constructive for problem: ", problemCtx)
    sol = ExampleSol()
    # print("count=", sys.getrefcount(sol)) # count=2
    for i in range(0, problemCtx.n):
        sol.bag.append(random.choice([0, 1]))
    sol.n = problemCtx.n
    print("\tfinished callback_constructive with sol: ", sol)
    return sol


class FEvaluator(object):

    def evaluate(self):
        return 30  # self.p

# =============================


class OptFrameEngine(object):
    def __init__(self):
        self.hf = fcore_lib.fcore_api1_create_engine()
        atexit.register(self.cleanup)

    def cleanup(self):
        print("Running optframe cleanup...")
        fcore_lib.fcore_api1_destroy_engine(self.hf)

    def print_component(self, component):
        fcore_lib.fcore_component_print(component)

    # =================== ADD =========================

    # register GeneralEvaluator (as FEvaluator) for min_callback
    def minimize(self, min_callback):
        idx_ev = fcore_lib.fcore_api1_add_float64_evaluator(
            self.hf,     FUNC_FEVALUATE(min_callback), True)
        return idx_ev

    def maximize(self, max_callback):
        idx_ev = fcore_lib.fcore_api1_add_float64_evaluator(
            self.hf,     FUNC_FEVALUATE(max_callback), False)
        return idx_ev

    def add_constructive(self, problemCtx, callback_constructive):
        print("add_constructive begins")
        idx_c = fcore_lib.fcore_api1_add_constructive(
            self.hf,     FUNC_FCONSTRUCTIVE(callback_constructive), problemCtx,
            FUNC_SOL_DEEPCOPY(callback_sol_deepcopy),
            FUNC_SOL_TOSTRING(callback_sol_tostring),
            FUNC_UTILS_DECREF(callback_utils_decref))
        print("add_constructive is finishing")
        return idx_c

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

    def fevaluator_evaluate(self, fevaluator_ptr: ctypes.py_object, min_or_max: bool, py_sol):
        pyo_view = ctypes.py_object(py_sol)
        z = fcore_lib.fcore_api1_float64_fevaluator_evaluate(
            fevaluator_ptr, min_or_max, pyo_view)
        return z

    def fconstructive_gensolution(self, fconstructive_ptr: ctypes.py_object) -> ctypes.py_object:
        #pyo_view = ctypes.py_object(py_sol)
        print("begin fconstructive_gensolution")
        pyo_sol = fcore_lib.fcore_api1_fconstructive_gensolution(
            fconstructive_ptr)
        print("finished fconstructive_gensolution!")
        # I THINK we must decref it... because it was once boxed into C++ solution and incref'ed somewhere...
        ctypes.pythonapi.Py_DecRef(pyo_sol)
        return pyo_sol.value


# ==============================

def callback_sol_print(sol: ExampleSol):
    print("sol = ", sol.foo())
    return 1


def callback_utils_incref(pyo: ctypes.py_object):
    print("callback_utils_incref: ", sys.getrefcount(pyo), " will get +1")
    ctypes.pythonapi.Py_IncRef(pyo)
    return sys.getrefcount(pyo)


def callback_utils_decref(pyo):
    print("callback_utils_decref: ", sys.getrefcount(pyo), " will get -1")
    print("pyo:", pyo)
    # IMPORTANT: 'pyo' may come as a Real Python Object, not a 'ctypes.py_object'
    cast_pyo = ctypes.py_object(pyo)
    ctypes.pythonapi.Py_DecRef(cast_pyo)
    return sys.getrefcount(pyo)


# ========

def test_memory():
    a = ExampleSol()
    #
    a.n = 11
    b1, b2 = copy(a), deepcopy(a)
    #
    a.n = 12
    a.bag.append(5)
    #
    print('a:', a.n, a.bag)
    print('b1:', b1.n, b1.bag)
    print('b2:', b2.n, b2.bag)
    #
    pyo = ctypes.py_object(a)
    # ctypes.pythonapi.Py_IncRef(pyo)  # will give reference to fcore_lib
    callback_utils_incref(pyo)
    #
    vcpp = fcore_lib.fcore_test_gensolution(
        pyo, FUNC_SOL_DEEPCOPY(callback_sol_deepcopy),
        FUNC_SOL_TOSTRING(callback_sol_tostring),
        FUNC_UTILS_DECREF(callback_utils_decref))
    vsol = fcore_lib.fcore_test_invokesolution(
        vcpp, FUNC_TEST(callback_sol_print))

    # ctypes.pythonapi.Py_IncRef(vsol)
    return vcpp


# =============================
#       BEGIN SCRIPT
# =============================
print("hello")

vcpp = test_memory()
print("vcpp=", vcpp)
vsol = fcore_lib.fcore_test_invokesolution(
    vcpp, FUNC_TEST(callback_sol_print))
print("vsol=", vsol)
print("")

#x = [10]
sol = ExampleSol()
print(sol)
print(sol.foo())
print(type(sol))
# 30
# <class '__main__.ExampleSol'>

#p_x = ctypes.cast(ctypes.py_object(x), ctypes.c_void_p)
# print(type(p_x))

fcore_lib.fcore_test_print_1(sol, 50)
# 0x7fb672864520 | 50

print("")
print("calling 'fcore_test_func'")
y = fcore_lib.fcore_test_func(sol, FUNC_TEST(mycallback), 50)
#0x7f8124256520 | 50
# From Python: callback
# <class '__main__.ExampleSol'>
# 0x7f8124256520 | func_out= 30 | 50

print("y=", y)
print("")
#fcore_lib.fcore_test_1(p_x, 50)

print("")
print("BEGIN SERIOUS Engine HF")
hf = fcore_lib.fcore_api1_create_engine()
print("Engine ptr=", hf)


# function evaluate(int[] v, int sz) -> int (evaluation)
#FUNC_EVALUATE = CFUNCTYPE(c_int, POINTER(c_int), c_int)

# https://stackoverflow.com/questions/50889988/the-attribute-of-ctypes-py-object
# ctypes.py_object ..

print("add evaluator")
idx_ev = fcore_lib.fcore_api1_add_float64_evaluator(
    hf,     FUNC_FEVALUATE(callback_fevaluate), True)
print("idx_ev=", idx_ev)

print("get general evaluator")
fevaluator = fcore_lib.fcore_api1_get_float64_evaluator(hf, idx_ev)

print("test print")
fcore_lib.fcore_component_print(fevaluator)
print("")

print("evaluate")
# giving ownership over 'sol' for function 'evaluate' to Box it
pyo_view = ctypes.py_object(sol)
# ctypes.pythonapi.Py_IncRef(pyo)  # TODO: do we need this? I hope not...
z = fcore_lib.fcore_api1_float64_fevaluator_evaluate(
    fevaluator, True, pyo_view)
print("finished evaluate")
print(z)
print("")

print("END SERIOUS Engine HF")
good = fcore_lib.fcore_api1_destroy_engine(hf)
print(good)

print("")
print("bye")
print("")

####################

print("BEGIN again with OptFrameEngine")
engine = OptFrameEngine()
pKP = ExampleKP()
pKP.n = 5
pKP.w = [1, 2, 3, 4, 5]
pKP.p = [5, 4, 3, 2, 1]
pKP.Q = 6.0
print(pKP)

ev_idx = engine.minimize(callback_fevaluate)
print("evaluator id:", ev_idx)
fev = engine.get_evaluator()
engine.print_component(fev)
#
print("")
sol = ExampleSol()
print(sol)
z = engine.fevaluator_evaluate(fev, True, sol)
#
print("")
print("==========================")
print("manually generate solution")
print("==========================")

s = callback_constructive(pKP)
print("")
print("count=", sys.getrefcount(s))
print(s)

print("")

c_idx = engine.add_constructive(pKP, callback_constructive)
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


exit(0)
