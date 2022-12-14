#!/usr/bin/python3

import ctypes
from ctypes import *
#
# too many options for handling resources in python libs... trying atexit
# https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
import atexit
#
from copy import deepcopy
import sys

import pathlib

from enum import Enum, IntEnum


# ==================== optframe_lib.so ===================

libfile = pathlib.Path(__file__).parent / "optframe_lib.so"
optframe_lib = ctypes.CDLL(str(libfile))

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


# -------------------------------------




# =====================================
#        OptFrame ADD Component
# =====================================

# problem*, solution* -> double
FUNC_FEVALUATE = CFUNCTYPE(ctypes.c_double, ctypes.py_object, ctypes.py_object)

# fcore_float64_fevaluator(void* hf, double (*_fevaluate)(void*), bool min_or_max) -> int (index)
optframe_lib.optframe_api1d_add_evaluator.argtypes = [
    ctypes.c_void_p, FUNC_FEVALUATE, c_bool, ctypes.py_object]
optframe_lib.optframe_api1d_add_evaluator.restype = ctypes.c_int32

# ----------

# problem* -> solution*
FUNC_FCONSTRUCTIVE = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object)

optframe_lib.optframe_api1d_add_constructive.argtypes = [
    ctypes.c_void_p, FUNC_FCONSTRUCTIVE, ctypes.py_object,
    FUNC_SOL_DEEPCOPY, FUNC_SOL_TOSTRING, FUNC_UTILS_DECREF]
optframe_lib.optframe_api1d_add_constructive.restype = ctypes.c_int32

FUNC_FCROSS = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)

optframe_lib.optframe_api0d_add_general_crossover.argtypes = [
    ctypes.c_void_p, FUNC_FCROSS, FUNC_FCROSS, ctypes.py_object,
    FUNC_SOL_DEEPCOPY, FUNC_SOL_TOSTRING, FUNC_UTILS_DECREF]
optframe_lib.optframe_api0d_add_general_crossover.restype = ctypes.c_int32


class LibArrayDouble(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),  
                ("v", ctypes.POINTER(ctypes.c_double))]

    def __str__(self):
        return f"LibArrayDouble(size={self.size};v={self.v};)"

# extern "C" int // error or not
# optframe_api0_set_array_double(int sz, double* vec, LibArrayDouble* lad_ptr)
optframe_lib.optframe_api0_set_array_double.argtypes = [
    ctypes.c_int, POINTER(ctypes.c_double), POINTER(LibArrayDouble)]
optframe_lib.optframe_api0_set_array_double.restype = ctypes.c_int32


FUNC_FDECODER_RK = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, LibArrayDouble)

optframe_lib.optframe_api1d_add_rk_decoder.argtypes = [
    ctypes.c_void_p, FUNC_FDECODER_RK, ctypes.py_object,
    FUNC_SOL_DEEPCOPY, FUNC_SOL_TOSTRING, FUNC_UTILS_DECREF]
optframe_lib.optframe_api1d_add_rk_decoder.restype = ctypes.c_int32


# problem* -> LibArrayDouble
FUNC_FCONSTRUCTIVE_RK = CFUNCTYPE(
    ctypes.c_int, ctypes.py_object, POINTER(LibArrayDouble))

# RK Constructive
# int (*_fconstructive)(FakePythonObjPtr, LibArrayDouble*)

optframe_lib.optframe_api1d_add_rk_constructive.argtypes = [
    ctypes.c_void_p, FUNC_FCONSTRUCTIVE_RK, ctypes.py_object]
optframe_lib.optframe_api1d_add_rk_constructive.restype = ctypes.c_int32



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

# problem*, solution* -> ims*
FUNC_FNSSEQ_IT_INIT = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, ctypes.py_object)

# problem*, ims* -> void
FUNC_FNSSEQ_IT_FIRST = CFUNCTYPE(
    None, ctypes.py_object, ctypes.py_object)

# problem*, ims* -> void
FUNC_FNSSEQ_IT_NEXT = CFUNCTYPE(
    None, ctypes.py_object, ctypes.py_object)

# problem*, ims* -> bool
FUNC_FNSSEQ_IT_ISDONE = CFUNCTYPE(
    ctypes.c_bool, ctypes.py_object, ctypes.py_object)

# problem*, ims* -> move*
FUNC_FNSSEQ_IT_CURRENT = CFUNCTYPE(
    ctypes.py_object, ctypes.py_object, ctypes.py_object)

# fns: hf*, func_ns, func_mv1, func_mv2, func_mv3, problem* -> int
optframe_lib.optframe_api1d_add_ns.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND, FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
optframe_lib.optframe_api1d_add_ns.restype = ctypes.c_int32

# fns: hf*, func_ns, func_mv1, func_mv2, func_mv3, problem* -> int
optframe_lib.optframe_api3d_add_ns_xmes.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND, FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
optframe_lib.optframe_api3d_add_ns_xmes.restype = ctypes.c_int32

# fns: hf*, func_ns, func_mv1, func_mv2, func_mv3, problem* -> int
optframe_lib.optframe_api1d_add_nsseq.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND,
    FUNC_FNSSEQ_IT_INIT, FUNC_FNSSEQ_IT_FIRST, FUNC_FNSSEQ_IT_NEXT, FUNC_FNSSEQ_IT_ISDONE, FUNC_FNSSEQ_IT_CURRENT,
    FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
optframe_lib.optframe_api1d_add_nsseq.restype = ctypes.c_int32

# ================================
#              CREATE
# ================================
optframe_lib.optframe_api1d_create_initial_search.argtypes = [
    ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32]
optframe_lib.optframe_api1d_create_initial_search.restype = ctypes.c_int32
#
optframe_lib.optframe_api1d_create_component_list.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_create_component_list.restype = ctypes.c_int32

# =================================
#            BUILD
# =================================

# for GlobalSearch
optframe_lib.optframe_api1d_build_global.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_build_global.restype = ctypes.c_int32

# for SingleObjSearch
optframe_lib.optframe_api1d_build_single.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_build_single.restype = ctypes.c_int32

# for LocalSearch
optframe_lib.optframe_api1d_build_local_search.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_build_local_search.restype = ctypes.c_int32

# for Component
optframe_lib.optframe_api1d_build_component.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_build_component.restype = ctypes.c_int32

# ====================================
#        OptFrame GET Component
# ====================================
optframe_lib.optframe_api0d_get_evaluator.argtypes = [
    ctypes.c_void_p, c_int32]
optframe_lib.optframe_api0d_get_evaluator.restype = ctypes.c_void_p
#
optframe_lib.optframe_api0d_get_constructive.argtypes = [
    ctypes.c_void_p, c_int32]
optframe_lib.optframe_api0d_get_constructive.restype = ctypes.c_void_p
###

# Engine: HeuristicFactory
optframe_lib.optframe_api1d_create_engine.argtypes = [ctypes.c_int]
optframe_lib.optframe_api1d_create_engine.restype = ctypes.c_void_p
#
optframe_lib.optframe_api1d_destroy_engine.argtypes = [ctypes.c_void_p]
optframe_lib.optframe_api1d_destroy_engine.restype = ctypes.c_bool
#
optframe_lib.optframe_api0d_engine_test.argtypes = [ctypes.c_void_p]
optframe_lib.optframe_api0d_engine_test.restype = ctypes.c_bool
#
optframe_lib.optframe_api0d_engine_welcome.argtypes = [ctypes.c_void_p]
optframe_lib.optframe_api0d_engine_welcome.restype = None

#
optframe_lib.optframe_api1d_engine_list_builders.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_engine_list_builders.restype = ctypes.c_int
#
optframe_lib.optframe_api1d_engine_list_components.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p]
optframe_lib.optframe_api1d_engine_list_components.restype = ctypes.c_int
#
optframe_lib.optframe_api1d_engine_check.argtypes = [
    ctypes.c_void_p]
optframe_lib.optframe_api1d_engine_check.restype = ctypes.c_bool
###

# fcore_raw_component_print(void* component);
optframe_lib.optframe_api0_component_print.argtypes = [c_void_p]

optframe_lib.optframe_api1d_engine_component_set_loglevel.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
optframe_lib.optframe_api1d_engine_component_set_loglevel.restype = ctypes.c_bool


class SearchStatus(Enum):
    NO_REPORT = 0x00
    FAILED = 0x01
    RUNNING = 0x02
    # RESERVED = 0x04
    IMPOSSIBLE = 0x08
    NO_SOLUTION = 0x10
    IMPROVEMENT = 0x20
    LOCAL_OPT = 0x40
    GLOBAL_OPT = 0x80


class SearchOutput(ctypes.Structure):
    _fields_ = [("status", ctypes.c_int),  # optframe.SearchStatus
                ("has_best", ctypes.c_bool),
                ("best_s", ctypes.py_object),
                ("best_e", ctypes.c_double)]

    def __str__(self):
        return f"SearchOutput(status={self.status};has_best={self.has_best};best_s={self.best_s};best_e={self.best_e};)"



#
optframe_lib.optframe_api0d_engine_simulated_annealing.argtypes = [
    ctypes.c_void_p]
optframe_lib.optframe_api0d_engine_simulated_annealing.restype = SearchOutput
#
optframe_lib.optframe_api0d_engine_simulated_annealing_params.argtypes = [
    ctypes.c_void_p, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_int, ctypes.c_double]
optframe_lib.optframe_api0d_engine_simulated_annealing_params.restype = SearchOutput
#
optframe_lib.optframe_api0d_engine_classic_nsgaii_params.argtypes = [
    ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double,
     ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
optframe_lib.optframe_api0d_engine_classic_nsgaii_params.restype = SearchStatus


# extern "C" LibSearchOutput
# fcore_api1_run_sos_search(FakeEnginePtr _engine, int sos_idx, double timelimit);

optframe_lib.optframe_api1d_run_sos_search.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
optframe_lib.optframe_api1d_run_sos_search.restype = SearchOutput

optframe_lib.optframe_api1d_run_global_search.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
optframe_lib.optframe_api1d_run_global_search.restype = SearchOutput


# ======================================
#              SPECIFIC
# ======================================

# fcore_float64_fevaluator_evaluate(void* _fevaluator, bool min_or_max, void* solution_ptr) -> double
optframe_lib.optframe_api0d_fevaluator_evaluate.argtypes = [
    c_void_p, c_bool, ctypes.py_object]
optframe_lib.optframe_api0d_fevaluator_evaluate.restype = ctypes.c_double

# fcore_api1_fconstructive_gensolution(void* _fconstructive) -> py_object solution
optframe_lib.optframe_api0_fconstructive_gensolution.argtypes = [
    c_void_p]
optframe_lib.optframe_api0_fconstructive_gensolution.restype = ctypes.py_object


# =========================
#     OptFrame Engine
# =========================

def callback_sol_deepcopy_utils(sol):
    # print("invoking 'callback_sol_deepcopy'... sol=", sol)
    if (isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert (False)
    sol2 = deepcopy(sol)
    return sol2

def callback_adapter_list_to_vecdouble(l: list) -> POINTER(c_double):
    if (not isinstance(l, list)):
        assert (False)
    lad = LibArrayDouble()
    lad.size = len(l)
    #
    seq = ctypes.c_double * len(l)
    arr = seq(*l)
    #
    optframe_lib.optframe_api0_set_array_double(len(l), arr, byref(lad))
    return lad.v

# optframe.APILevel
class APILevel(Enum):
    API1d = "1d"  # API 1 for double type


# optframe.LogLevel
class LogLevel(IntEnum):
    Silent = 0
    Error = 1
    Warning = 2
    Info = 3
    Debug = 4
# example:
# if (loglevel >= LogLevel::Warning) { ... }


# optframe.Engine
class Engine(object):
    def __init__(self, apilevel: APILevel = APILevel.API1d, loglevel: LogLevel = LogLevel.Info):
        self.loglevel = loglevel
        ll_int = int(self.loglevel)
        assert (apilevel == APILevel.API1d)
        if (loglevel >= LogLevel.Debug):
            print("Debug: Engine using API level API1d")
        self.hf = optframe_lib.optframe_api1d_create_engine(ll_int)
        self.callback_sol_deepcopy_ptr = FUNC_SOL_DEEPCOPY(
            callback_sol_deepcopy_utils)
        self.callback_sol_tostring_ptr = FUNC_SOL_TOSTRING(
            callback_sol_tostring)
        self.callback_utils_decref_ptr = FUNC_UTILS_DECREF(
            callback_utils_decref)
            
        # keep callbacks in memory
        self.callback_list = []
        atexit.register(self.cleanup)

    def register_callback(self, func):
        # expects 'func' to be of ctypes.CFUNCTYPE
        # must keep callbacks in memory, otherwise Python cleans them...
        # TODO: pass callbacks with IncRef, so that we can keep them on C++ counterpart objects...
        # TODO: think if unique_ptr<std::function<...>> is an interesting pattern of OptFCore C++
        # TODO: for now, just keep them here.
        self.callback_list.append(func)

    def cleanup(self):
        if (self.loglevel >= LogLevel.Debug):
            print("Running optframe cleanup...")
        optframe_lib.optframe_api1d_destroy_engine(self.hf)

    def welcome(self):
        optframe_lib.optframe_api0d_engine_welcome(self.hf)

    def print_component(self, component):
        optframe_lib.optframe_api0_component_print(component)

    def component_set_loglevel(self, scomponent, loglevel, recursive):
        if (not isinstance(scomponent, str)):
            assert (False)
        b_comp = scomponent.encode('ascii')
        return optframe_lib.optframe_api1d_engine_component_set_loglevel(self.hf, b_comp, loglevel, recursive)

    def list_builders(self, pattern: str):
        if (not isinstance(pattern, str)):
            assert (False)
        b_pattern = pattern.encode('ascii')
        # type of b_pattern is 'bytes'
        # print("bytes type: ", type(b_pattern))
        return optframe_lib.optframe_api1d_engine_list_builders(self.hf, ctypes.c_char_p(b_pattern))

    def list_components(self, pattern: str):
        if (not isinstance(pattern, str)):
            assert (False)
        b_pattern = pattern.encode('ascii')
        # type of b_pattern is 'bytes'
        # print("bytes type: ", type(b_pattern))
        return optframe_lib.optframe_api1d_engine_list_components(self.hf, ctypes.c_char_p(b_pattern))

    def run_sa(self):
        print("DEPRECATED")
        print("Will Begin SA")
        r = optframe_lib.optframe_api1d_engine_simulated_annealing(self.hf)
        print("Finished SA")
        return r

    def run_sa_params(self, timelimit, id_ev, id_c, id_ns, alpha, iter, T):
        print("Will Begin SA Params")
        r = optframe_lib.optframe_api1d_engine_simulated_annealing_params(self.hf,
                                                                          timelimit, id_ev, id_c, id_ns,
                                                                          alpha, iter, T)
        print("Finished SA Params")
        return r

    def run_nsgaii_params(self, timelimit, min_limit, max_limit, id_mev, id_popman, popsize, maxiter):
        print("Will Begin NSGA-II Params")
        st = optframe_lib.optframe_api0d_engine_classic_nsgaii_params(self.hf,
                                                                    timelimit, min_limit, max_limit,
                                                                    id_mev, id_popman, popsize, maxiter)
        print("Finished NSGA-II Params")
        return st
        
    def run_test(self):
        print("Will Begin Test")
        r = optframe_lib.optframe_api1d_engine_test(self.hf)
        print("Finished Test")
        return r

    def check(self, p1: int, p2: int, verbose=False) -> bool:
        return optframe_lib.optframe_api1d_engine_check(self.hf, p1, p2, verbose)

    # =================== ADD =========================

    # register GeneralEvaluator (as FEvaluator) for min_callback
    def minimize(self, problemCtx, min_callback):
        min_callback_ptr = FUNC_FEVALUATE(min_callback)
        self.register_callback(min_callback_ptr)
        #
        idx_ev = optframe_lib.optframe_api1d_add_evaluator(
            self.hf, min_callback_ptr, True, problemCtx)
        return idx_ev

    def maximize(self, problemCtx, max_callback):
        max_callback_ptr = FUNC_FEVALUATE(max_callback)
        self.register_callback(max_callback_ptr)
        #
        idx_ev = optframe_lib.optframe_api1d_add_evaluator(
            self.hf, max_callback_ptr, False, problemCtx)
        return idx_ev

    def add_constructive(self, problemCtx, constructive_callback):
        constructive_callback_ptr = FUNC_FCONSTRUCTIVE(constructive_callback)
        self.register_callback(constructive_callback_ptr)
        #
        idx_c = optframe_lib.optframe_api1d_add_constructive(
            self.hf, constructive_callback_ptr, problemCtx,
            self.callback_sol_deepcopy_ptr,
            self.callback_sol_tostring_ptr,
            self.callback_utils_decref_ptr)
        return idx_c

    def add_crossover(self, problemCtx, cross_callback0, cross_callback1):
        cross_callback0_ptr = FUNC_FCROSS(cross_callback0)
        cross_callback1_ptr = FUNC_FCROSS(cross_callback1)
        self.register_callback(cross_callback0_ptr)
        self.register_callback(cross_callback1_ptr)
        #
        idx_c = optframe_lib.optframe_api0d_add_general_crossover(
            self.hf, cross_callback0_ptr, cross_callback0_ptr,
            problemCtx,
            self.callback_sol_deepcopy_ptr,
            self.callback_sol_tostring_ptr,
            self.callback_utils_decref_ptr)
        return idx_c

    def add_constructive_rk(self, problemCtx, constructive_rk_callback):
        #print("will execute 'add_constructive_rk'")
        #
        #print("will create lambda")
        #     ctypes.py_object -> LibArrayDouble
        #myfunction = lambda problem : callback_adapter_list_to_vecdouble(constructive_rk_callback(problem))
        # TODO: create own mapping function here, from List to ctypes double pointer
        #print("taking pointer from lambda")
        #constructive_rk_callback_ptr = FUNC_FCONSTRUCTIVE_RK(myfunction)
        #
        #
        #self.register_callback(constructive_rk_callback_ptr)
        constructive_rk_callback_ptr = FUNC_FCONSTRUCTIVE_RK(constructive_rk_callback)
        self.register_callback(constructive_rk_callback_ptr)
        #
        idx_c = optframe_lib.optframe_api1d_add_rk_constructive(
            self.hf, constructive_rk_callback_ptr, problemCtx)
        return idx_c

    def add_decoder_rk(self, problemCtx, decoder_rk_callback):
        decoder_rk_callback_ptr = FUNC_FDECODER_RK(decoder_rk_callback)
        self.register_callback(decoder_rk_callback_ptr)
        #
        idx_dec = optframe_lib.optframe_api1d_add_rk_decoder(
            self.hf, decoder_rk_callback_ptr, 
            problemCtx,
            self.callback_sol_deepcopy_ptr,
            self.callback_sol_tostring_ptr,
            self.callback_utils_decref_ptr)
        return idx_dec



    def add_ns(self, problemCtx, ns_rand_callback, move_apply_callback, move_eq_callback, move_cba_callback, isXMES=False):
        ns_rand_callback_ptr = FUNC_FNS_RAND(ns_rand_callback)
        self.register_callback(ns_rand_callback_ptr)
        #
        move_apply_callback_ptr = FUNC_FMOVE_APPLY(move_apply_callback)
        self.register_callback(move_apply_callback_ptr)
        move_eq_callback_ptr = FUNC_FMOVE_EQ(move_eq_callback)
        self.register_callback(move_eq_callback_ptr)
        move_cba_callback_ptr = FUNC_FMOVE_CBA(move_cba_callback)
        self.register_callback(move_cba_callback_ptr)
        #
        idx_ns = -1
        # if NOT Multi Objective
        if not isXMES:
            idx_ns = optframe_lib.optframe_api1d_add_ns(
                self.hf, ns_rand_callback_ptr, move_apply_callback_ptr,
                move_eq_callback_ptr, move_cba_callback_ptr, problemCtx,
                self.callback_utils_decref_ptr)
        else: # this is Multi Objective
            idx_ns = optframe_lib.optframe_api3d_add_ns_xmes(
                self.hf, ns_rand_callback_ptr, move_apply_callback_ptr,
                move_eq_callback_ptr, move_cba_callback_ptr, problemCtx,
                self.callback_utils_decref_ptr)
        return idx_ns

    def add_nsseq(self, problemCtx,
                  ns_rand_callback,
                  nsseq_it_init_callback, nsseq_it_first_callback, nsseq_it_next_callback, nsseq_it_isdone_callback, nsseq_it_current_callback,
                  move_apply_callback, move_eq_callback, move_cba_callback):
        ns_rand_callback_ptr = FUNC_FNS_RAND(ns_rand_callback)
        self.register_callback(ns_rand_callback_ptr)
        #
        nsseq_it_init_callback_ptr = FUNC_FNSSEQ_IT_INIT(
            nsseq_it_init_callback)
        self.register_callback(nsseq_it_init_callback_ptr)
        nsseq_it_first_callback_ptr = FUNC_FNSSEQ_IT_FIRST(
            nsseq_it_first_callback)
        self.register_callback(nsseq_it_first_callback_ptr)
        nsseq_it_next_callback_ptr = FUNC_FNSSEQ_IT_NEXT(
            nsseq_it_next_callback)
        self.register_callback(nsseq_it_next_callback_ptr)
        nsseq_it_isdone_callback_ptr = FUNC_FNSSEQ_IT_ISDONE(
            nsseq_it_isdone_callback)
        self.register_callback(nsseq_it_isdone_callback_ptr)
        nsseq_it_current_callback_ptr = FUNC_FNSSEQ_IT_CURRENT(
            nsseq_it_current_callback)
        self.register_callback(nsseq_it_current_callback_ptr)
        #
        move_apply_callback_ptr = FUNC_FMOVE_APPLY(move_apply_callback)
        self.register_callback(move_apply_callback_ptr)
        move_eq_callback_ptr = FUNC_FMOVE_EQ(move_eq_callback)
        self.register_callback(move_eq_callback_ptr)
        move_cba_callback_ptr = FUNC_FMOVE_CBA(move_cba_callback)
        self.register_callback(move_cba_callback_ptr)
        #
        idx_nsseq = optframe_lib.optframe_api1d_add_nsseq(
            self.hf, ns_rand_callback_ptr,
            nsseq_it_init_callback_ptr,
            nsseq_it_first_callback_ptr,
            nsseq_it_next_callback_ptr,
            nsseq_it_isdone_callback_ptr,
            nsseq_it_current_callback_ptr,
            move_apply_callback_ptr,
            move_eq_callback_ptr, move_cba_callback_ptr, problemCtx,
            self.callback_utils_decref_ptr)

        return idx_nsseq

    # =============================
    #            CREATE
    # =============================

    def create_initial_search(self, ev_idx, c_idx):
        idx_is = optframe_lib.optframe_api1d_create_initial_search(
            self.hf, ev_idx, c_idx)
        return idx_is

    def create_component_list(self, str_list, str_type):
        if (not isinstance(str_list, str)):
            assert (False)
        b_list = str_list.encode('ascii')
        if (not isinstance(str_type, str)):
            assert (False)
        b_type = str_type.encode('ascii')
        #
        idx_list = optframe_lib.optframe_api1d_create_component_list(
            self.hf, b_list, b_type)
        return idx_list

    # =========================
    #         BUILD
    # =========================

    def build_global_search(self, str_builder, str_params):
        if (not isinstance(str_builder, str)):
            assert (False)
        b_builder = str_builder.encode('ascii')
        if (not isinstance(str_params, str)):
            assert (False)
        b_params = str_params.encode('ascii')
        #
        idx_list = optframe_lib.optframe_api1d_build_global(
            self.hf, b_builder, b_params)
        return idx_list

    def build_single_obj_search(self, str_builder, str_params):
        if (not isinstance(str_builder, str)):
            assert (False)
        b_builder = str_builder.encode('ascii')
        if (not isinstance(str_params, str)):
            assert (False)
        b_params = str_params.encode('ascii')
        #
        idx_list = optframe_lib.optframe_api1d_build_single(
            self.hf, b_builder, b_params)
        return idx_list

    def build_local_search(self, str_builder, str_params):
        if (not isinstance(str_builder, str)):
            assert (False)
        b_builder = str_builder.encode('ascii')
        if (not isinstance(str_params, str)):
            assert (False)
        b_params = str_params.encode('ascii')
        #
        idx_list = optframe_lib.optframe_api1d_build_local_search(
            self.hf, b_builder, b_params)
        return idx_list

    def build_component(self, str_builder, str_params, str_component_type):
        if (not isinstance(str_builder, str)):
            assert (False)
        b_builder = str_builder.encode('ascii')
        if (not isinstance(str_params, str)):
            assert (False)
        b_params = str_params.encode('ascii')
        if (not isinstance(str_component_type, str)):
            assert (False)
        b_ctype = str_component_type.encode('ascii')
        #
        idx_comp = optframe_lib.optframe_api1d_build_component(
            self.hf, b_builder, b_params, b_ctype)
        return idx_comp

    # ===================== GET =======================

    def get_evaluator(self, idx_ev=0):
        fevaluator = optframe_lib.optframe_api0d_get_evaluator(
            self.hf, idx_ev)
        return fevaluator

    def get_constructive(self, idx_c=0):
        fconstructive = optframe_lib.optframe_api0d_get_constructive(
            self.hf, idx_c)
        return fconstructive

    # ==================================================
    # non-standard non-api method... just for testing
    # ==================================================

    def fevaluator_evaluate(self, fevaluator_ptr: ctypes.py_object, min_or_max: bool, py_sol):
        # print("invoking 'optframe_lib.optframe_api1d_float64_fevaluator_evaluate' with fevaluator_ptr=", fevaluator_ptr)
        # self.print_component(fevaluator_ptr)
        pyo_view = ctypes.py_object(py_sol)
        # print("begin fevaluator_evaluate with pyo_view=", pyo_view)
        z = optframe_lib.optframe_api0d_fevaluator_evaluate(
            fevaluator_ptr, min_or_max, pyo_view)
        # print("'fevaluator_evaluate' final z=", z)
        return z

    def fconstructive_gensolution(self, fconstructive_ptr: ctypes.py_object) -> ctypes.py_object:
        # print("XXXXX BEGIN 'fconstructive_gensolution'")
        # print("invoking 'optframe_lib.optframe_api1d_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)
        # print("printing component... => ")
        #self.print_component(fconstructive_ptr)

        # print("begin fconstructive_gensolution")
        pyo_sol = optframe_lib.optframe_api0_fconstructive_gensolution(
            fconstructive_ptr)
        # print("finished invoking 'optframe_lib.optframe_api1d_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)

        # print("pyo_sol=", pyo_sol, " count=", sys.getrefcount(pyo_sol))
        #
        # I THINK we must decref it... because it was once boxed into C++ solution and incref'ed somewhere...
        #
        cast_pyo = ctypes.py_object(pyo_sol)
        # print("cast_pyo=", cast_pyo, " count=", sys.getrefcount(cast_pyo))
        # ERROR: when decref, it segfaults... don't know why
        # ctypes.pythonapi.Py_DecRef(cast_pyo)
        # print("finished invoking 'optframe_lib.optframe_api1d_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)
        #
        #
        # print("XXXXX FINISHED 'fconstructive_gensolution'!")
        return cast_pyo.value

    def run_global_search(self, g_idx, timelimit) -> SearchOutput:
        lout = optframe_lib.optframe_api1d_run_global_search(
            self.hf, g_idx, timelimit)
        # l2out = SearchOutput(lout)
        return lout

    def run_sos_search(self, sos_idx, timelimit) -> SearchOutput:
        lout = optframe_lib.optframe_api1d_run_sos_search(
            self.hf, sos_idx, timelimit)
        # l2out = SearchOutput(lout)
        return lout


# ==============================

# def callback_utils_incref(pyo: ctypes.py_object):
#    # print("callback_utils_incref: ", sys.getrefcount(pyo), " will get +1")
#    ctypes.pythonapi.Py_IncRef(pyo)
#    return sys.getrefcount(pyo)

def callback_utils_decref(pyo):
    if (isinstance(pyo, ctypes.py_object)):
        pyo = pyo.value
        print("pyo:", pyo)
    # print("callback_utils_decref: ", sys.getrefcount(pyo), " will get -1")
    # IMPORTANT: 'pyo' may come as a Real Python Object, not a 'ctypes.py_object'
    cast_pyo = ctypes.py_object(pyo)
    #
    ctypes.pythonapi.Py_DecRef(cast_pyo)
    x = sys.getrefcount(pyo)
    return x


def callback_sol_tostring(sol, pt: ctypes.c_char_p, ptsize: ctypes.c_size_t):
    mystr = sol.__str__()
    mystr_bytes = mystr.encode()
    pa = cast(pt, POINTER(c_char * ptsize))
    pa.contents.value = mystr_bytes
    return len(mystr)

# ==============================
