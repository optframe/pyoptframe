#ifndef fcore_LIB_H
#define fcore_LIB_H

#include <cstdint> // int32_t
#include <stdio.h>

typedef void* FakeFEvaluatorPtr;
typedef void* FakeFConstructivePtr;
typedef void* FakePythonObjPtr;
typedef void* FakeEnginePtr;

// ============================ Engine: HeuristicFactory ===========================

extern "C" FakeEnginePtr
fcore_api1_create_engine();

extern "C" bool
fcore_api1_destroy_engine(FakeEnginePtr hf);

// ============

extern "C" int // index of generalevaluator
fcore_api1_add_float64_evaluator(FakeEnginePtr _hf,
                                 double (*_fevaluate)(FakePythonObjPtr, FakePythonObjPtr),
                                 bool min_or_max,
                                 FakePythonObjPtr problem_view);

extern "C" int // index of constructive
fcore_api1_add_constructive(FakeEnginePtr _hf,
                            FakePythonObjPtr (*_fconstructive)(FakePythonObjPtr),
                            FakePythonObjPtr problem_view,
                            FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
                            size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
                            int (*f_utils_decref)(FakePythonObjPtr));

extern "C" int // index of ns
fcore_api1_add_ns(FakeEnginePtr _hf,
                  FakePythonObjPtr (*_fns_rand)(FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr (*_fmove_apply)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_eq)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_cba)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr problem_view,
                  int (*f_utils_decref)(FakePythonObjPtr));

// ================

extern "C" void* // raw (non-owned) pointer to GeneralEvaluator
fcore_api1_get_float64_evaluator(FakeEnginePtr _hf, int idx_ev);

extern "C" void* // raw (non-owned) pointer to Constructive
fcore_api1_get_constructive(FakeEnginePtr _hf, int idx_c);

// ===============

// SPECIFIC

extern "C" double
fcore_float64_fevaluator_evaluate(FakeFEvaluatorPtr fevaluator, bool min_or_max, FakePythonObjPtr solution_ptr);

extern "C" FakePythonObjPtr // Python solution object (owned??? by who?? maybe non-owned, but alive...)
fcore_api1_fconstructive_gensolution(FakeFConstructivePtr _fconstructive);

// ============================ COMPONENT ===========================
extern "C" void
fcore_component_print(void* component);

// ============================

#endif // fcore_LIB_H
