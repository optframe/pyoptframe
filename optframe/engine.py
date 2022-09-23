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

import pathlib

# ==================== fcore_lib.so ===================

libfile = pathlib.Path(__file__).parent / "fcore_lib.so"

# manual setup ?
if(False):
    fcore_lib = ctypes.cdll.LoadLibrary('../build/fcore_lib.so')
else:
    fcore_lib = ctypes.CDLL(str(libfile))

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
fcore_lib.fcore_api1_add_ns.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND, FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
fcore_lib.fcore_api1_add_ns.restype = ctypes.c_int32

# fns: hf*, func_ns, func_mv1, func_mv2, func_mv3, problem* -> int
fcore_lib.fcore_api1_add_nsseq.argtypes = [
    ctypes.c_void_p, FUNC_FNS_RAND,
    FUNC_FNSSEQ_IT_INIT, FUNC_FNSSEQ_IT_FIRST, FUNC_FNSSEQ_IT_NEXT, FUNC_FNSSEQ_IT_ISDONE, FUNC_FNSSEQ_IT_CURRENT,
    FUNC_FMOVE_APPLY, FUNC_FMOVE_EQ, FUNC_FMOVE_CBA, ctypes.py_object, FUNC_UTILS_DECREF]
fcore_lib.fcore_api1_add_nsseq.restype = ctypes.c_int32

# ================================
#              CREATE
# ================================
fcore_lib.fcore_api1_create_initial_search.argtypes = [
    ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32]
fcore_lib.fcore_api1_create_initial_search.restype = ctypes.c_int32
#
fcore_lib.fcore_api1_create_component_list.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
fcore_lib.fcore_api1_create_component_list.restype = ctypes.c_int32

# =================================
#            BUILD
# =================================

# for SingleObjSearch
fcore_lib.fcore_api1_build_single.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
fcore_lib.fcore_api1_build_single.restype = ctypes.c_int32

# for LocalSearch
fcore_lib.fcore_api1_build_local_search.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
fcore_lib.fcore_api1_build_local_search.restype = ctypes.c_int32

# for Component
fcore_lib.fcore_api1_build_component.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
fcore_lib.fcore_api1_build_component.restype = ctypes.c_int32

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
fcore_lib.fcore_api1_engine_builders.argtypes = [
    ctypes.c_void_p,  ctypes.c_char_p]
fcore_lib.fcore_api1_engine_builders.restype = ctypes.c_int
#
fcore_lib.fcore_api1_engine_list_components.argtypes = [
    ctypes.c_void_p,  ctypes.c_char_p]
fcore_lib.fcore_api1_engine_list_components.restype = ctypes.c_int
#
fcore_lib.fcore_api1_engine_check.argtypes = [
    ctypes.c_void_p]
fcore_lib.fcore_api1_engine_check.restype = ctypes.c_bool
###

#fcore_raw_component_print(void* component);
fcore_lib.fcore_raw_component_print.argtypes = [c_void_p]

fcore_lib.fcore_api1_engine_component_set_loglevel.argtypes = [
    ctypes.c_void_p,  ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
fcore_lib.fcore_api1_engine_component_set_loglevel.restype = ctypes.c_bool


class SearchOutput(ctypes.Structure):
    _fields_ = [("status", c_int),
                ("has_best", ctypes.c_bool),
                ("best_s", ctypes.py_object),
                ("best_e", ctypes.c_double)]

    def __str__(self):
        return f"SearchOutput(status={self.status};has_best={self.has_best};best_s={self.best_s};best_e={self.best_e};)"


#
fcore_lib.fcore_api1_engine_simulated_annealing.argtypes = [ctypes.c_void_p]
fcore_lib.fcore_api1_engine_simulated_annealing.restype = SearchOutput
#
fcore_lib.fcore_api1_engine_simulated_annealing_params.argtypes = [
    ctypes.c_void_p,  ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_int, ctypes.c_double]
fcore_lib.fcore_api1_engine_simulated_annealing_params.restype = SearchOutput

# extern "C" LibSearchOutput
# fcore_api1_run_sos_search(FakeEnginePtr _engine, int sos_idx, double timelimit);

fcore_lib.fcore_api1_run_sos_search.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
fcore_lib.fcore_api1_run_sos_search.restype = SearchOutput


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

def callback_sol_deepcopy_utils(sol):
    #print("invoking 'callback_sol_deepcopy'... sol=", sol)
    if(isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert(False)
    sol2 = deepcopy(sol)
    return sol2


class OptFrameEngine(object):
    def __init__(self):
        self.hf = fcore_lib.fcore_api1_create_engine()
        self.callback_sol_deepcopy_ptr = FUNC_SOL_DEEPCOPY(
            callback_sol_deepcopy_utils)
        self.callback_sol_tostring_ptr = FUNC_SOL_TOSTRING(
            callback_sol_tostring)
        self.callback_utils_decref_ptr = FUNC_UTILS_DECREF(
            callback_utils_decref)
        atexit.register(self.cleanup)

    def cleanup(self):
        print("Running optframe cleanup...")
        fcore_lib.fcore_api1_destroy_engine(self.hf)

    def print_component(self, component):
        fcore_lib.fcore_raw_component_print(component)

    def component_set_loglevel(self, scomponent, loglevel, recursive):
        if(not isinstance(scomponent, str)):
            assert(False)
        b_comp = scomponent.encode('ascii')
        return fcore_lib.fcore_api1_engine_component_set_loglevel(self.hf, b_comp, loglevel, recursive)

    def list_builders(self, pattern: str):
        if(not isinstance(pattern, str)):
            assert(False)
        b_pattern = pattern.encode('ascii')
        # type of b_pattern is 'bytes'
        #print("bytes type: ", type(b_pattern))
        return fcore_lib.fcore_api1_engine_builders(self.hf, ctypes.c_char_p(b_pattern))

    def list_components(self, pattern: str):
        if(not isinstance(pattern, str)):
            assert(False)
        b_pattern = pattern.encode('ascii')
        # type of b_pattern is 'bytes'
        #print("bytes type: ", type(b_pattern))
        return fcore_lib.fcore_api1_engine_list_components(self.hf, ctypes.c_char_p(b_pattern))

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

    def add_nsseq(self, problemCtx,
                  ns_rand_callback_ptr,
                  nsseq_it_init_callback_ptr,
                  nsseq_it_first_callback_ptr,
                  nsseq_it_next_callback_ptr,
                  nsseq_it_isdone_callback_ptr,
                  nsseq_it_current_callback_ptr,
                  ###########
                  move_apply_callback_ptr, move_eq_callback_ptr, move_cba_callback_ptr):
        #print("add_ns begins")
        idx_nsseq = fcore_lib.fcore_api1_add_nsseq(
            self.hf,  ns_rand_callback_ptr,
            nsseq_it_init_callback_ptr,
            nsseq_it_first_callback_ptr,
            nsseq_it_next_callback_ptr,
            nsseq_it_isdone_callback_ptr,
            nsseq_it_current_callback_ptr,
            move_apply_callback_ptr,
            move_eq_callback_ptr, move_cba_callback_ptr, problemCtx,
            self.callback_utils_decref_ptr)
        # FUNC_UTILS_DECREF(callback_utils_decref))
        #print("add_ns is finishing")
        return idx_nsseq

    # =============================
    #            CREATE
    # =============================

    def create_initial_search(self, ev_idx, c_idx):
        #print("create_initial_search begins")
        idx_is = fcore_lib.fcore_api1_create_initial_search(
            self.hf, ev_idx, c_idx)
        return idx_is

    def create_component_list(self, str_list, str_type):
        if(not isinstance(str_list, str)):
            assert(False)
        b_list = str_list.encode('ascii')
        if(not isinstance(str_type, str)):
            assert(False)
        b_type = str_type.encode('ascii')
        #
        idx_list = fcore_lib.fcore_api1_create_component_list(
            self.hf, b_list, b_type)
        return idx_list

    # =========================
    #         BUILD
    # =========================

    def build_single_obj_search(self, str_builder, str_params):
        if(not isinstance(str_builder, str)):
            assert(False)
        b_builder = str_builder.encode('ascii')
        if(not isinstance(str_params, str)):
            assert(False)
        b_params = str_params.encode('ascii')
        #
        idx_list = fcore_lib.fcore_api1_build_single(
            self.hf, b_builder, b_params)
        return idx_list

    def build_local_search(self, str_builder, str_params):
        if(not isinstance(str_builder, str)):
            assert(False)
        b_builder = str_builder.encode('ascii')
        if(not isinstance(str_params, str)):
            assert(False)
        b_params = str_params.encode('ascii')
        #
        idx_list = fcore_lib.fcore_api1_build_local_search(
            self.hf, b_builder, b_params)
        return idx_list

    def build_component(self, str_builder, str_params, str_component_type):
        if(not isinstance(str_builder, str)):
            assert(False)
        b_builder = str_builder.encode('ascii')
        if(not isinstance(str_params, str)):
            assert(False)
        b_params = str_params.encode('ascii')
        if(not isinstance(str_component_type, str)):
            assert(False)
        b_ctype = str_component_type.encode('ascii')
        #
        idx_comp = fcore_lib.fcore_api1_build_component(
            self.hf, b_builder, b_params, b_ctype)
        return idx_comp

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
        #print("XXXXX BEGIN 'fconstructive_gensolution'")
        #print("invoking 'fcore_lib.fcore_api1_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)
        #print("printing component... => ")
        self.print_component(fconstructive_ptr)

        #print("begin fconstructive_gensolution")
        pyo_sol = fcore_lib.fcore_api1_fconstructive_gensolution(
            fconstructive_ptr)
        #print("finished invoking 'fcore_lib.fcore_api1_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)

        #print("pyo_sol=", pyo_sol, " count=", sys.getrefcount(pyo_sol))
        #
        # I THINK we must decref it... because it was once boxed into C++ solution and incref'ed somewhere...
        #
        cast_pyo = ctypes.py_object(pyo_sol)
        #print("cast_pyo=", cast_pyo, " count=", sys.getrefcount(cast_pyo))
        # ERROR: when decref, it segfaults... don't know why
        # ctypes.pythonapi.Py_DecRef(cast_pyo)
        ###print("finished invoking 'fcore_lib.fcore_api1_fconstructive_gensolution' with fconstructive_ptr=", fconstructive_ptr)
        #
        #
        #print("XXXXX FINISHED 'fconstructive_gensolution'!")
        return cast_pyo.value

    def run_sos_search(self, sos_idx, timelimit) -> SearchOutput:
        lout = fcore_lib.fcore_api1_run_sos_search(self.hf, sos_idx, timelimit)
        #l2out = SearchOutput(lout)
        return lout


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


def callback_sol_tostring(sol, pt: ctypes.c_char_p, ptsize: ctypes.c_size_t):
    mystr = sol.__str__()  # + '\0'
    mystr_bytes = mystr.encode()  # str.encode(mystr)
    pa = cast(pt, POINTER(c_char * ptsize))
    pa.contents.value = mystr_bytes
    #print("\tPYTHON TOSTRING callback_sol_tostring: '", mystr, "'")
    return len(mystr)

# ==============================
