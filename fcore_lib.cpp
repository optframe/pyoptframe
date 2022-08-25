#include "fcore_lib.h"
//

#include <assert.h>
#include <iostream>

#include <OptFCore/FCore.hpp>
#include <OptFCore/FxCore.hpp>
#include <OptFrame/HeuristicFactory.hpp>
#include <OptFrame/MyConcepts.hpp> // sref

class FCoreLibSolution
{
public:
   // 'solution_ptr' is internal representation/solution pointer
   // note that the pointer can be a view (is_view=1) or an owned reference that needs decref (is_view=0)
   FakePythonObjPtr solution_ptr;
   // is view: when is_view=1, no decref is needed
   bool is_view;
   // copy constructor function
   std::function<FakePythonObjPtr(FakePythonObjPtr)> f_sol_deepcopy;
   // print/to string function
   std::function<int(FakePythonObjPtr, char*, int)> f_sol_tostring;
   // utils function
   std::function<bool(FakePythonObjPtr)> f_utils_decref;

   FCoreLibSolution(const FCoreLibSolution& s)
   {
      //std::cout << "FCoreLibSolution(COPY)" << std::endl;
      assert(s.solution_ptr);
      assert(!s.is_view); // because of deepcopy anyway... COULD we copy a view here? I don't think so..
      //std::cout << "\tFCoreLibSolution(COPY)-> will copy functions" << std::endl;
      // copy functions
      this->f_sol_deepcopy = s.f_sol_deepcopy;
      this->f_utils_decref = s.f_utils_decref;
      // copy flags
      this->is_view = s.is_view;
      //std::cout << "\tFCoreLibSolution(COPY)-> will deepcopy" << std::endl;
      // perform deepcopy and IncRef
      this->solution_ptr = this->f_sol_deepcopy(s.solution_ptr);
      //std::cout << "\tFCoreLibSolution(COPY; ptr1_origin=" << s.solution_ptr << "; ptr2_dest=" << this->solution_ptr << ")" << std::endl;
   }

   FCoreLibSolution(FCoreLibSolution&& s)
   {
      //std::cout << "FCoreLibSolution(MOVE)" << std::endl;
      assert(s.solution_ptr);
      // copy flags
      this->is_view = s.is_view;
      if (!s.is_view) {
         //std::cout << "\tNOT_VIEW! FCoreLibSolution(MOVE)-> will move functions" << std::endl;
         // copy functions
         this->f_sol_deepcopy = std::move(s.f_sol_deepcopy);
         this->f_utils_decref = std::move(s.f_utils_decref);
      }
      //std::cout << "\tFCoreLibSolution(MOVE)-> will steal pointer" << std::endl;
      this->solution_ptr = s.solution_ptr;
      // prepare corpse
      s.solution_ptr = 0;
      s.is_view = true;
      //
      //std::cout << "\tFCoreLibSolution(MOVE finished; ptr=" << solution_ptr << ")" << std::endl;
   }

   virtual ~FCoreLibSolution()
   {
      //std::cout << "~FCoreLibSolution is_view = " << this->is_view << " ptr: " << solution_ptr << std::endl;
      //
      if (!this->is_view) {
         // must decref solution_ptr and discard it
         int x = f_utils_decref(solution_ptr);
         //std::cout << "~FCoreLibSolution ptr count = " << x << std::endl;
      }
      solution_ptr = nullptr;
      //std::cout << "~FCoreLibSolution finished" << std::endl;
   }

   //FCoreLibSolution(FakePythonObjPtr solution_ptr, std::function<FakePythonObjPtr(FakePythonObjPtr)> copy_solution)
   FCoreLibSolution(FakePythonObjPtr solution_ptr,
                    std::function<FakePythonObjPtr(FakePythonObjPtr)> f_sol_deepcopy,
                    std::function<int(FakePythonObjPtr, char*, int)> f_sol_tostring,
                    std::function<int(FakePythonObjPtr)> f_utils_decref)
     : solution_ptr{ solution_ptr }
     , is_view{ false }
     , f_sol_deepcopy{ f_sol_deepcopy }
     , f_sol_tostring{ f_sol_tostring }
     , f_utils_decref{ f_utils_decref }
   //, copy_solution{ copy_solution }
   {
      //printf("FCoreLibSolution3(%p, func, func, func) is_view=%d\n", solution_ptr, is_view);
      //std::cout << "\tFCoreLibSolution3->C++ str: '" << toString() << "'" << std::endl;
   }

   // temporary construction (no copy_solution required)

   FCoreLibSolution(FakePythonObjPtr solution_ptr_view)
     : solution_ptr{ solution_ptr_view }
     , is_view{ true }
   {
      //printf("FCoreLibSolution1(%p) is_view=%d\n", solution_ptr, is_view);
   }

   std::string toString() const
   {
      constexpr int max_buffer = 100;
      //
      std::string str_buffer(max_buffer, '\0');
      //std::cout << "size = " << str_buffer.size() << std::endl;
      //std::cout << "str_buffer => '" << str_buffer << "'" << std::endl;
      //
      char* s_ptr = &str_buffer[0];
      int sz = f_sol_tostring(solution_ptr, s_ptr, str_buffer.size());
      //std::cout << "toString spent sz=" << sz << " from max=" << max_buffer << std::endl;
      std::string str_ret(s_ptr, s_ptr + sz);
      //assert(str_ret.size() == sz);
      return str_ret;
   }
};

using FCoreLibESolution = std::pair<FCoreLibSolution, optframe::Evaluation<double>>;

// ============================ Engine: HeuristicFactory ===========================

using FCoreApi1Engine = optframe::HeuristicFactory<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;

extern "C" FakeHeuristicFactoryPtr
fcore_api1_create_engine()
{
   FakeHeuristicFactoryPtr hf_ptr = new FCoreApi1Engine;
   return hf_ptr;
}

extern "C" bool
fcore_api1_destroy_engine(FakeHeuristicFactoryPtr _hf)
{
   auto* hf = (FCoreApi1Engine*)_hf;
   delete hf;
   // good
   return true;
}

// ==============================================
//                      ADD
// ==============================================

// min_or_max is needed to correctly cast template on FEvaluator
extern "C" int // index of generalevaluator
fcore_api1_add_float64_evaluator(FakeHeuristicFactoryPtr _hf, double (*_fevaluate)(FakePythonObjPtr), bool min_or_max)
{
   auto* hf = (FCoreApi1Engine*)_hf;
   //printf("hf=%p\n", (void*)hf);

   auto fevaluate = [_fevaluate](const FCoreLibSolution& s) -> optframe::Evaluation<double> {
      //printf("will invoke _fevaluate(%p) over s.solution_ptr = %p\n", (void*)_fevaluate, s.solution_ptr);
      double r = _fevaluate(s.solution_ptr);
      //printf("return r=%f\n", r);
      return r;
   };

   int id = -1;
   if (min_or_max) {
      // Minimization
      sref<optframe::Component> eval(
        new optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MINIMIZE>{ fevaluate });
      //std::cout << "created FEvaluator<MIN> ptr=" << &eval.get() << std::endl;
      id = hf->addComponent(eval, "OptFrame:GeneralEvaluator");
   } else {
      // Maximization
      sref<optframe::Component> eval(
        new optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MAXIMIZE>{ fevaluate });

      id = hf->addComponent(eval, "OptFrame:GeneralEvaluator");
   }

   return id;
}

// IMPORTANT: method 'add_constructive' receives a 'problem_view', while a 'problem_owned' would be desired...
// However, this would require an extra 'int (*f_utils_decref)(FakePythonObjPtr)', but it's doable.
// Worse, this would also require some personalization of std::function destructor over FConstructive,
// or a change in FConstructor to allow personalized destructors...
// Maybe, at this moment, we just require that 'problem_view' must exist at the time constructive is invoked.
// We can somehow ensure this on Python, which prevents extra referencing counting on both sides.
// On Python, storing it on the engine (or the opposite) may do the job for us, so, no worry for now.

extern "C" int // index of constructive
fcore_api1_add_constructive(FakeHeuristicFactoryPtr _hf,
                            FakePythonObjPtr (*_fconstructive)(FakePythonObjPtr),
                            FakePythonObjPtr problem_view,
                            // Support necessary for Solution construction and maintainance
                            FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
                            size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
                            int (*f_utils_decref)(FakePythonObjPtr))
{
   auto* hf = (FCoreApi1Engine*)_hf;

   //std::cout << "invoking 'fcore_api1_add_constructive' with "
   //          << "_hf=" << _hf << " _fconstructive and problem_view=" << problem_view << std::endl;

   auto fconstructive = [_fconstructive,
                         problem_view,
                         f_sol_deepcopy,
                         f_sol_tostring,
                         f_utils_decref]() -> FCoreLibSolution {
      // IMPORTANT: _fconstructive must IncRef before returning! I think so...
      FakePythonObjPtr vobj_owned = _fconstructive(problem_view);
      //std::cout << "'fcore_api1_add_constructive' -> _fconstructive generated pointer: " << vobj_owned << std::endl;
      assert(vobj_owned); // check void* (TODO: for FxConstructive, return nullopt)
      FCoreLibSolution sol(vobj_owned, f_sol_deepcopy, f_sol_tostring, f_utils_decref);
      //std::cout << "'fcore_api1_add_constructive' -> solution created!" << std::endl;
      return sol;
   };

   sref<optframe::Component> fc(
     new optframe::FConstructive<FCoreLibSolution>{ fconstructive });

   //std::cout << "'fcore_api1_add_constructive' will add component on hf" << std::endl;

   int id = hf->addComponent(fc, "OptFrame:Constructive");
   //std::cout << "c_id = " << id << std::endl;
   //fc->print();
   return id;
}

// ==============================================
//                      GET
// ==============================================

extern "C" void* // raw (non-owned) pointer to GeneralEvaluator
fcore_api1_get_float64_evaluator(FakeHeuristicFactoryPtr _hf, int idx_ev)
{
   auto* hf = (FCoreApi1Engine*)_hf;

   std::shared_ptr<optframe::GeneralEvaluator<FCoreLibESolution, FCoreLibESolution::second_type>> component;

   hf->assignGE(component, idx_ev, "OptFrame:GeneralEvaluator");
   if (!component)
      assert(false);
   void* ptr = component.get();
   return ptr;
}

extern "C" void* // raw (non-owned) pointer to FConstructive
fcore_api1_get_constructive(FakeHeuristicFactoryPtr _hf, int idx_c)
{
   auto* hf = (FCoreApi1Engine*)_hf;

   std::shared_ptr<optframe::Constructive<FCoreLibSolution>> component;

   hf->assign(component, idx_c, "OptFrame:Constructive");
   if (!component)
      assert(false);
   void* ptr = component.get();
   return ptr;
}

// ==============================================
//            SPECIFIC INVOCATIONS
// ==============================================

// min_or_max is needed to correctly cast template on FEvaluator
extern "C" double //FEvaluator object
fcore_api1_float64_fevaluator_evaluate(FakeFEvaluatorPtr _fevaluator, bool min_or_max, FakePythonObjPtr solution_ptr_view)
{
   FCoreLibSolution sol(solution_ptr_view);
   optframe::Evaluation<double> ev(0);
   if (min_or_max) {
      // MINIMIZE
      auto* fevaluator = (optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MINIMIZE>*)_fevaluator;
      ev = fevaluator->evaluate(sol);
   } else {
      // MAXIMIZE
      auto* fevaluator = (optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MAXIMIZE>*)_fevaluator;
      ev = fevaluator->evaluate(sol);
   }
   return ev.evaluation();
}

extern "C" FakePythonObjPtr // Python solution object
fcore_api1_fconstructive_gensolution(FakeFConstructivePtr _fconstructive)
{
   //std::cout << "begin 'fcore_api1_fconstructive_gensolution'" << std::endl;
   auto* fconstructive = (optframe::FConstructive<FCoreLibSolution>*)_fconstructive;
   std::optional<FCoreLibSolution> sol = fconstructive->generateSolution(0.0);
   //std::cout << "will check if optional solution exists: " << !!sol << std::endl;
   assert(sol);
   // will return solution to Python... must make sure it will live!
   // should IncRef it here?? Perhaps...
   // will move it out from boxed Sol object, and make it a fake is_view=1 object here.
   FakePythonObjPtr ptr = sol->solution_ptr;
   //std::cout << "finished 'fcore_api1_fconstructive_gensolution'... returning ptr=" << ptr << std::endl;
   // ======= "kill" sol container =======
   sol->solution_ptr = 0;
   sol->is_view = 1;
   return ptr;
}

// ==============

extern "C" void
fcore_component_print(void* component)
{
   auto* c = (optframe::Component*)component;
   //std::cout << "fcore_component_print ptr=" << c << " => ";
   c->print();
}

// ==============================================
