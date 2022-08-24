#ifndef fcore_LIB_H
#define fcore_LIB_H

#include <cstdint> // int32_t
#include <stdio.h>

typedef void* FakeFEvaluatorPtr;
typedef void* FakeFConstructivePtr;
typedef void* FakePythonObjPtr;
typedef void* FakeHeuristicFactoryPtr;

// test if python object is received, plus an int
extern "C" int32_t
fcore_test_print_1(FakePythonObjPtr vpython, int32_t sz_vr);

// test if func is received
extern "C" int32_t
fcore_test_func(FakePythonObjPtr vpython, int32_t (*func)(void*), int32_t sz_vr);

// test storage and memory
extern "C" FakePythonObjPtr
fcore_test_gensolution(
  FakePythonObjPtr vpython,
  FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
  size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
  int (*f_utils_decref)(FakePythonObjPtr) // TODO: remove this?
);

// =========================== FEVALUATOR ===========================
// constructor
extern "C" FakeFEvaluatorPtr // returns FEvaluator object
fcore_new_float64_fevaluator(double (*_fevaluate)(FakePythonObjPtr), bool min_or_max);

extern "C" double
fcore_float64_fevaluator_evaluate(FakeFEvaluatorPtr fevaluator, bool min_or_max, FakePythonObjPtr solution_ptr);

// ============================ Engine: HeuristicFactory ===========================

extern "C" FakeHeuristicFactoryPtr
fcore_api1_create_engine();

extern "C" bool
fcore_api1_destroy_engine(FakeHeuristicFactoryPtr hf);

// ============

extern "C" int // index of generalevaluator
fcore_api1_add_float64_evaluator(FakeHeuristicFactoryPtr _hf, double (*_fevaluate)(FakePythonObjPtr), bool min_or_max);

extern "C" void* // raw (non-owned) pointer to GeneralEvaluator
fcore_api1_get_float64_evaluator(FakeHeuristicFactoryPtr _hf, int idx_ev);

// ==============

extern "C" int // index of constructive
fcore_api1_add_constructive(FakeHeuristicFactoryPtr _hf,
                            FakePythonObjPtr (*_fconstructive)(FakePythonObjPtr),
                            FakePythonObjPtr problem_view,
                            FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
                            size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
                            int (*f_utils_decref)(FakePythonObjPtr));

extern "C" void* // raw (non-owned) pointer to Constructive
fcore_api1_get_constructive(FakeHeuristicFactoryPtr _hf, int idx_c);

extern "C" FakePythonObjPtr // Python solution object (owned??? by who?? maybe non-owned, but alive...)
fcore_api1_fconstructive_gensolution(FakeFConstructivePtr _fconstructive);

// ============================ COMPONENT ===========================
extern "C" void
fcore_component_print(void* component);

extern "C" void
fcore_component_free(void* component); // IMPOSSIBLE!

// ============================

#endif // fcore_LIB_H
