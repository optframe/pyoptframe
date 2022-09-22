#ifndef fcore_LIB_H
#define fcore_LIB_H

#include <cstdint> // int32_t
#include <stdio.h>

typedef void* FakeFEvaluatorPtr;
typedef void* FakeFConstructivePtr;
typedef void* FakeFNSPtr;
typedef void* FakePythonObjPtr;
typedef void* FakeEnginePtr;

// ============= compatible api components =============

extern "C" struct LibSearchOutput
{
   int status;    // ("status", c_int),
   bool has_best; // ("has_best", ctypes.c_bool),
   void* best_s;  // ("best_s", ctypes.py_object),
   double best_e; // ("best_e", ctypes.c_double)]
};

// ============================ Engine: HeuristicFactory ===========================

extern "C" FakeEnginePtr
fcore_api1_create_engine();

extern "C" bool
fcore_api1_engine_check(FakeEnginePtr _engine, int p1, int p2, bool verbose);

extern "C" LibSearchOutput
fcore_api1_engine_simulated_annealing(FakeEnginePtr _engine);
// double alpha, int iter, double temp

extern "C" LibSearchOutput
fcore_api1_engine_simulated_annealing_params(FakeEnginePtr _engine, double timelimit, int id_evaluator, int id_constructive, int id_ns, double alpha, int iter, double T);
// double alpha, int iter, double temp

extern "C" int
fcore_api1_engine_builders(FakeEnginePtr _engine, char* prefix);

extern "C" int
fcore_api1_engine_list_components(FakeEnginePtr _engine, char* prefix);

extern "C" bool
fcore_api1_engine_test(FakeEnginePtr _engine);

extern "C" bool
fcore_api1_destroy_engine(FakeEnginePtr _engine);

// ============

extern "C" int // index of generalevaluator
fcore_api1_add_float64_evaluator(FakeEnginePtr _engine,
                                 double (*_fevaluate)(FakePythonObjPtr, FakePythonObjPtr),
                                 bool min_or_max,
                                 FakePythonObjPtr problem_view);

extern "C" int // index of constructive
fcore_api1_add_constructive(FakeEnginePtr _engine,
                            FakePythonObjPtr (*_fconstructive)(FakePythonObjPtr),
                            FakePythonObjPtr problem_view,
                            FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
                            size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
                            int (*f_utils_decref)(FakePythonObjPtr));

extern "C" int // index of ns
fcore_api1_add_ns(FakeEnginePtr _engine,
                  FakePythonObjPtr (*_fns_rand)(FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr (*_fmove_apply)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_eq)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_cba)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr problem_view,
                  int (*f_utils_decref)(FakePythonObjPtr));

// CREATE

extern "C" int // index of ComponentList
fcore_api1_create_component_list(FakeEnginePtr _engine, char* clist, char* list_type);

extern "C" int // index of InitialSearch
fcore_api1_create_initial_search(FakeEnginePtr _engine, int ev_idx, int c_idx);

// BUILD

extern "C" int // index of SingleObjSearch
fcore_api1_build_single(FakeEnginePtr _engine, char* builder, char* build_string);

extern "C" int // index of LocalSearch
fcore_api1_build_local_search(FakeEnginePtr _engine, char* builder, char* build_string);

extern "C" int // index of Component
fcore_api1_build_component(FakeEnginePtr _engine, char* builder, char* build_string, char* component_type);

// ================

extern "C" void* // raw (non-owned) pointer to GeneralEvaluator
fcore_api1_get_float64_evaluator(FakeEnginePtr _engine, int idx_ev);

extern "C" void* // raw (non-owned) pointer to Constructive
fcore_api1_get_constructive(FakeEnginePtr _hf, int idx_c);

// ===============

// SPECIFIC / INVOKE

extern "C" double
fcore_float64_fevaluator_evaluate(FakeFEvaluatorPtr fevaluator, bool min_or_max, FakePythonObjPtr solution_ptr);

extern "C" FakePythonObjPtr // Python solution object (owned??? by who?? maybe non-owned, but alive...)
fcore_api1_fconstructive_gensolution(FakeFConstructivePtr _fconstructive);

// RUN

extern "C" LibSearchOutput // SearchOutput for XSH "best-type"
fcore_api1_run_sos_search(FakeEnginePtr _engine, int sos_idx, double timelimit);

// ============================ COMPONENT ===========================
extern "C" void
fcore_component_print(void* component);

// ============================

#endif // fcore_LIB_H
