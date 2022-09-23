#include "fcore_lib.h"
//

#include <assert.h>
#include <iostream>

#include <OptFCore/FCore.hpp>
#include <OptFCore/FxCore.hpp>
#include <OptFrame/HeuristicFactory.hpp>
#include <OptFrame/Loader.hpp>
#include <OptFrame/MyConcepts.hpp> // sref
#include <OptFrame/OptFrameList.hpp>
#include <OptFrame/Util/CheckCommand.hpp>

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
      this->f_sol_tostring = s.f_sol_tostring;
      this->f_utils_decref = s.f_utils_decref;
      // copy flags
      this->is_view = s.is_view;
      //std::cout << "\tFCoreLibSolution(COPY)-> will deepcopy" << std::endl;
      // perform deepcopy and IncRef
      this->solution_ptr = this->f_sol_deepcopy(s.solution_ptr);
      //std::cout << "\tFCoreLibSolution(COPY; ptr1_origin=" << s.solution_ptr << "; ptr2_dest=" << this->solution_ptr << ")" << std::endl;
   }

   FCoreLibSolution& operator=(const FCoreLibSolution& other)
   {
      if (this == &other)
         return *this;

      assert(other.solution_ptr);
      assert(!other.is_view); // because of deepcopy anyway... COULD we copy a view here? I don't think so..
      // copy functions
      this->f_sol_deepcopy = other.f_sol_deepcopy;
      this->f_sol_tostring = other.f_sol_tostring;
      this->f_utils_decref = other.f_utils_decref;
      // copy flags
      this->is_view = other.is_view;

      // will decref current copy of solution
      if (!this->is_view) {
         // must decref solution_ptr and discard it
         int x = f_utils_decref(solution_ptr);
         if (x > 1) {
            std::cout << "operator=(FCoreLibSolution) ptr_count = " << x << std::endl;
         }
      }
      solution_ptr = nullptr;

      // perform deepcopy and IncRef
      this->solution_ptr = this->f_sol_deepcopy(other.solution_ptr);
      return *this;
   }

   FCoreLibSolution& operator=(FCoreLibSolution&& other)
   {
      //std::cout << "ERROR! Could not find a use-case for move solution... is there one?" << std::endl;
      //assert(false);
      if (this == &other)
         return *this;

      assert(other.solution_ptr);
      // copy functions
      this->f_sol_deepcopy = other.f_sol_deepcopy;
      this->f_sol_tostring = other.f_sol_tostring;
      this->f_utils_decref = other.f_utils_decref;
      // copy flags
      this->is_view = other.is_view;

      // steal pointer from corpse
      this->solution_ptr = other.solution_ptr;
      // kill it
      other.solution_ptr = 0;
      other.is_view = 1;
      return *this;
   }

   FCoreLibSolution(FCoreLibSolution&& s)
   {
      //std::cout << "FCoreLibSolution(MOVE) BEGIN" << std::endl;
      assert(s.solution_ptr);
      //std::cout << "FCoreLibSolution(MOVE).other.toString() -> '" << s.toString() << "'" << std::endl;

      // copy flags
      this->is_view = s.is_view;
      if (!s.is_view) {
         //std::cout << "\tNOT_VIEW! FCoreLibSolution(MOVE)-> will move functions" << std::endl;
         // copy functions OR MOVE???? TODO....
         this->f_sol_deepcopy = std::move(s.f_sol_deepcopy);
         this->f_sol_tostring = std::move(s.f_sol_tostring);
         this->f_utils_decref = std::move(s.f_utils_decref);
      }
      //std::cout << "\tFCoreLibSolution(MOVE)-> will steal pointer" << std::endl;
      this->solution_ptr = s.solution_ptr;
      // prepare corpse
      s.solution_ptr = 0;
      s.is_view = true;
      //
      //std::cout << "\tFCoreLibSolution(MOVE).toString() -> '" << toString() << "'" << std::endl;
      //std::cout << "\tFCoreLibSolution(MOVE finished; ptr=" << solution_ptr << ")" << std::endl;
      //std::cout << "FCoreLibSolution(MOVE) ENDS" << std::endl;
   }

   virtual ~FCoreLibSolution()
   {
      //std::cout << "~FCoreLibSolution is_view = " << this->is_view << " ptr: " << solution_ptr << std::endl;
      //
      if (!this->is_view) {
         assert(solution_ptr);
         // must decref solution_ptr and discard it
         int x = f_utils_decref(solution_ptr);
         //std::cout << "~FCoreLibSolution ptr_count = " << x << std::endl;
         if (x > 1) {
            std::cout << "~FCoreLibSolution ptr_count = " << x << std::endl;
         }
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
      //std::string str = toString();
      //std::cout << "\tFCoreLibSolution3->C++ str: '" << str << "'" << std::endl;
   }

   // temporary construction (no copy_solution required)

   FCoreLibSolution(FakePythonObjPtr solution_ptr_view)
     : solution_ptr{ solution_ptr_view }
     , is_view{ true }
   {
      //printf("FCoreLibSolution1(%p) is_view=%d\n", solution_ptr, is_view);
   }

   FakePythonObjPtr releasePtr()
   {
      // pointer must exist
      assert(this->solution_ptr);
      // cannot take this from view
      assert(!this->is_view);
      FakePythonObjPtr sol = this->solution_ptr;
      // "move" from this container
      this->solution_ptr = nullptr;
      this->is_view = true;
      // TODO: do we need to remove the functions too?
      return sol;
   }

   std::string toString() const
   {
      //std::cout << "WILL PRINT! is_view=" << is_view << " ptr=" << solution_ptr << std::endl;
      constexpr int max_buffer = 10'000; // TODO: MAKE THIS FLEXIBLE!!!
      //
      std::string str_buffer(max_buffer, '\0');
      //std::cout << "size = " << str_buffer.size() << std::endl;
      //std::cout << "str_buffer => '" << str_buffer << "'" << std::endl;
      //
      char* s_ptr = &str_buffer[0];
      int sz = f_sol_tostring(solution_ptr, s_ptr, str_buffer.size());
      assert(sz < max_buffer);
      //std::cout << "toString spent sz=" << sz << " from max=" << max_buffer << std::endl;
      std::string str_ret(s_ptr, s_ptr + sz);
      //assert(str_ret.size() == sz);
      //std::cout << "finished print!" << std::endl;
      return str_ret;
   }

   friend std::ostream& operator<<(std::ostream& os, const FCoreLibSolution& me)
   {
      os << me.toString();
      return os;
   }
};

using FCoreLibESolution = std::pair<FCoreLibSolution, optframe::Evaluation<double>>;

// ============================ Engine: HeuristicFactory ===========================

/*
using FCoreApi1Engine = optframe::HeuristicFactory<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;
*/

using CB = optframe::ComponentBuilder<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;

using CBSingle = optframe::SingleObjSearchBuilder<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;

using CBLocal = optframe::LocalSearchBuilder<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;

using CB = optframe::ComponentBuilder<
  FCoreLibSolution,             //XSolution S,
  optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
  FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
  //X2ESolution<XES> X2ES = MultiESolution<XES>>
  >;

class FCoreApi1Engine
{
public:
   /*
   optframe::HeuristicFactory<
     FCoreLibSolution,             //XSolution S,
     optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
     FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
     //X2ESolution<XES> X2ES = MultiESolution<XES>>
     >
     hf;
     */

   optframe::Loader<
     FCoreLibSolution,             //XSolution S,
     optframe::Evaluation<double>, // XEvaluation XEv = Evaluation<>,
     FCoreLibESolution             //  XESolution XES = pair<S, XEv>,
     //X2ESolution<XES> X2ES = MultiESolution<XES>>
     >
     loader;

   optframe::CheckCommand<FCoreLibESolution> check; // no verbose
};

// IMPORTANT: OptFrame FMove does not require Copy on M (aka, FakePythonObjPtr)... I HOPE!
// Don't remember needing a clone() member on OptFrame Moves... but nice to clarify a NoCopy (NoNothing...) concept there.
//using FMoveLib = optframe::FMove<FakePythonObjPtr, FCoreLibESolution>;

// will not use FMove now, because of DecRef on destructor... a necessary personalization.

class FMoveLib : public optframe::Move<FCoreLibESolution, typename FCoreLibESolution::second_type>
{
   using XES = FCoreLibESolution;
   using XEv = typename XES::second_type;
   using XSH = XES; // only single objective
   using M = FakePythonObjPtr;

public:
   M m; // internal structure for move

   typedef std::function<M(const M&, XES&)> FuncTypeMoveApply;
   typedef std::function<bool(const M&, const XES&)> FuncTypeMoveCBA;
   typedef std::function<bool(const M&, const Move<XES>&)> FuncTypeMoveEq;
   typedef std::function<bool(FakePythonObjPtr)> FuncTypeUtilsDecRef;

   //M (*fApply)(const M&, XES&);                    // fApply
   FuncTypeMoveApply fApply;
   //bool (*fCanBeApplied)(const M&, const XES&) ;   // fCanBeApplied
   FuncTypeMoveCBA fCanBeApplied;
   //bool (*fCompareEq)(const M&, const Move<XES>&); // fCompareEq
   FuncTypeMoveEq fCompareEq;
   // utils for decref
   FuncTypeUtilsDecRef f_utils_decref;

   FMoveLib(
     M _m_owned, // must IncRef before passing here...
     //M (*_fApply)(const M&, XES&),                   // fApply
     const FuncTypeMoveApply& _fApply,
     //bool (*_fCanBeApplied)(const M&, const XES&) ,  // fCanBeApplied
     const FuncTypeMoveCBA& _fCanBeApplied,
     //bool (*_fCompareEq)(const M&, const Move<XES>&) // fCompareEq
     const FuncTypeMoveEq& _fCompareEq,
     // decref utils
     const FuncTypeUtilsDecRef& _f_utils_decref)
     : m{ _m_owned }
     , fApply{ _fApply }
     , fCanBeApplied{ _fCanBeApplied }
     , fCompareEq{ _fCompareEq }
     , f_utils_decref{ _f_utils_decref }
   {
   }

   virtual ~FMoveLib()
   {
      //std::cout << "~FMoveLib()" << std::endl;
      //int x =
      f_utils_decref(m);
      //std::cout << "~FMoveLib count(m) = " << x << std::endl;
   }

   virtual bool canBeApplied(const XES& se) override
   {
      return fCanBeApplied(m, se);
   }

   virtual optframe::uptr<Move<XES, XEv, XSH>> apply(XSH& se) override
   {
      return optframe::uptr<Move<XES, XEv, XSH>>{
         new FMoveLib{ fApply(m, se), fApply, fCanBeApplied, fCompareEq, f_utils_decref }
      };
   }

   virtual bool operator==(const Move<XES, XEv, XSH>& move) const override
   {
      const Move<XES>& move2 = (Move<XES>&)move;
      return fCompareEq(this->m, move2);
   }

   bool operator!=(const Move<XES, XEv, XSH>& m) const
   {
      return !(*this == m);
   }

   static string idComponent()
   {
      std::stringstream ss;
      ss << Component::idComponent() << ":FMoveLib";
      return ss.str();
   }

   virtual string id() const override
   {
      return idComponent();
   }

   // use 'operator<<' for M
   virtual void print() const override
   {
      std::cout << m << std::endl;
   }
};

// Iterator object for NSSeqIterator
class IMSObjLib
{
public:
   // 'ims_ptr' is internal representation/solution pointer
   FakePythonObjPtr ims_ptr;
   // utils function
   std::function<bool(FakePythonObjPtr)> f_utils_decref;

   IMSObjLib(const IMSObjLib& s) = delete;
   IMSObjLib& operator=(const IMSObjLib& other) = delete;

   IMSObjLib& operator=(IMSObjLib&& other)
   {
      // is this possible?
      if (this == &other)
         return *this;
      // check if other exists
      assert(other.ims_ptr);
      // copy functions
      this->f_utils_decref = other.f_utils_decref;
      // steal pointer from corpse
      this->ims_ptr = other.ims_ptr;
      // kill it
      other.ims_ptr = 0;
      return *this;
   }

   IMSObjLib(IMSObjLib&& s)
   {
      //std::cout << "IMSObjLib(MOVE) BEGIN" << std::endl;
      assert(s.ims_ptr);
      //std::cout << "IMSObjLib(MOVE).other.toString() -> '" << s.toString() << "'" << std::endl;

      // copy
      this->f_utils_decref = std::move(s.f_utils_decref);

      //std::cout << "\tIMSObjLib(MOVE)-> will steal pointer" << std::endl;
      this->ims_ptr = s.ims_ptr;
      // prepare corpse
      s.ims_ptr = 0;
      //
      //std::cout << "\tIMSObjLib(MOVE finished; ptr=" << ims_ptr << ")" << std::endl;
      //std::cout << "IMSObjLib(MOVE) ENDS" << std::endl;
   }

   virtual ~IMSObjLib()
   {
      //std::cout << "~IMSObjLib ptr: " << ims_ptr << std::endl;
      //
      if (this->ims_ptr) {
         // must decref solution_ptr and discard it
         int x = f_utils_decref(this->ims_ptr);
         //std::cout << "~FCoreLibSolution ptr_count = " << x << std::endl;
         if (x > 1) {
            std::cout << "~IMSObjLib ptr_count = " << x << std::endl;
         }

         ims_ptr = 0;
      }
      //std::cout << "~IMSObjLib finished" << std::endl;
   }

   IMSObjLib(FakePythonObjPtr ims_ptr, std::function<int(FakePythonObjPtr)> f_utils_decref)
     : ims_ptr{ ims_ptr }
     , f_utils_decref{ f_utils_decref }
   {
      //printf("IMSObjLib1(%p, func)\n", ims_ptr);
   }

   // temporary construction (no copy_solution required)
   /*
   FCoreLibSolution(FakePythonObjPtr solution_ptr_view)
     : solution_ptr{ solution_ptr_view }
     , is_view{ true }
   {
      //printf("FCoreLibSolution1(%p) is_view=%d\n", solution_ptr, is_view);
   }
   */

   /*
   FakePythonObjPtr
   releasePtr()
   {
      // pointer must exist
      assert(this->solution_ptr);
      // cannot take this from view
      assert(!this->is_view);
      FakePythonObjPtr sol = this->solution_ptr;
      // "move" from this container
      this->solution_ptr = nullptr;
      this->is_view = true;
      // TODO: do we need to remove the functions too?
      return sol;
   }
   */
};

// ==================

extern "C" FakeEnginePtr
fcore_api1_create_engine()
{
   FakeEnginePtr engine_ptr = new FCoreApi1Engine;
   return engine_ptr;
}

extern "C" bool
fcore_api1_engine_check(FakeEnginePtr _engine, int p1, int p2, bool verbose)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   engine->check.setParameters(verbose);
   // bool run(int iterMax, int nSolNSSeq)
   auto data = engine->check.run(p1, p2);
   return true;
}

extern "C" LibSearchOutput
fcore_api1_engine_simulated_annealing(FakeEnginePtr _engine)
{
   return fcore_api1_engine_simulated_annealing_params(_engine, 3.0, 0, 0, 0, 0.99, 100, 9999);
}

extern "C" int
fcore_api1_engine_builders(FakeEnginePtr _engine, char* prefix)
{
   std::string sprefix{ prefix };
   auto* engine = (FCoreApi1Engine*)_engine;
   std::vector<std::pair<std::string, std::vector<std::pair<std::string, std::string>>>>
     vlist = engine->loader.factory.listBuilders(sprefix);
   for (auto& p : vlist) {
      std::cout << "builder: " << p.first << " |params|=" << p.second.size() << std::endl;
      for (unsigned i = 0; i < p.second.size(); i++)
         std::cout << "\tparam " << i << " => " << p.second[i].first << " : " << p.second[i].second << std::endl;
   }
   return vlist.size();
}

extern "C" int
fcore_api1_engine_list_components(FakeEnginePtr _engine, char* prefix)
{
   std::string sprefix{ prefix };
   auto* engine = (FCoreApi1Engine*)_engine;
   std::vector<std::string> vlist = engine->loader.factory.listComponents(sprefix);
   for (unsigned i = 0; i < vlist.size(); i++)
      std::cout << "component " << i << " => " << vlist[i] << std::endl;
   return vlist.size();
}

extern "C" int // index of ComponentList
fcore_api1_create_component_list(FakeEnginePtr _engine, char* clist, char* list_type)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   //
   std::string str_list{ clist };
   std::string str_type{ list_type };
   //
   std::map<std::string, std::vector<std::string>> ldictionary; // TODO: why??
   //
   std::vector<std::string>* vvlist = optframe::OptFrameList::readList(ldictionary, str_list);
   //std::cout << "lsit size=" << vvlist->size() << std::endl;
   std::cout << vvlist->at(0) << std::endl;
   std::vector<sptr<optframe::Component>> vcomp;
   for (unsigned i = 0; i < vvlist->size(); i++) {
      sptr<optframe::Component> comp;
      scannerpp::Scanner scanComp{ vvlist->at(i) };
      std::string sid = scanComp.next();
      int cid = *scanComp.nextInt();
      engine->loader.factory.assign(comp, cid, sid);
      vcomp.push_back(comp);
   }
   delete vvlist;

   int id = engine->loader.factory.addComponentList(vcomp, str_type);
   return id;
}

extern "C" LibSearchOutput
fcore_api1_engine_simulated_annealing_params(FakeEnginePtr _engine, double timelimit, int id_evaluator, int id_constructive, int id_ns, double alpha, int iter, double T)
{
   auto* engine = (FCoreApi1Engine*)_engine;

   //
   using MyEval = optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>;

   // will try to get evaluator to build InitialSolution component...
   std::shared_ptr<MyEval> _ev;
   engine->loader.factory.assign(_ev, id_evaluator, "OptFrame:GeneralEvaluator:Evaluator");
   assert(_ev);
   sref<MyEval> single_ev{ _ev };
   //
   //
   using MyConstructive = optframe::Constructive<FCoreLibSolution>;
   //
   std::shared_ptr<MyConstructive> initial;
   engine->loader.factory.assign(initial, id_constructive, "OptFrame:Constructive");
   assert(initial);
   //
   sref<optframe::InitialSearch<FCoreLibESolution>> initSol{
      new optframe::BasicInitialSearch<FCoreLibESolution>(initial, single_ev)
   };
   //
   using MyNS = optframe::NS<FCoreLibESolution, optframe::Evaluation<double>>;
   //
   std::shared_ptr<MyNS> ns;
   engine->loader.factory.assign(ns, id_ns, "OptFrame:NS");
   assert(ns);
   //

   sref<optframe::RandGen> rg = engine->loader.factory.getRandGen();

   //sref<optframe::GeneralEvaluator<FCoreLibESolution, optframe::Evaluation<double>>> evaluator{ gev };
   sref<optframe::InitialSearch<FCoreLibESolution, optframe::Evaluation<double>>> constructive{ initSol };
   vsref<optframe::NS<FCoreLibESolution, optframe::Evaluation<double>>> neighbors;
   neighbors.push_back(ns);

   single_ev->print();
   constructive->print();
   neighbors[0]->print();

   optframe::BasicSimulatedAnnealing<FCoreLibESolution> sa{
      single_ev, constructive, neighbors, alpha, iter, T, rg
   };
   sa.setVerbose();

   optframe::SearchOutput<FCoreLibESolution> out = sa.search({ timelimit });
   //std::cout << "out=" << out.status << std::endl;

   LibSearchOutput lout;
   lout.status = (int)out.status;  // ("status", c_int),
   lout.has_best = (bool)out.best; // ("has_best", ctypes.c_bool),
   if (out.best) {
      // extract pointer from solution container
      lout.best_s = out.best->first.releasePtr();  // ("best_s", ctypes.py_object),
      lout.best_e = out.best->second.evaluation(); // ("best_e", ctypes.c_double)]
   }
   return lout;
}

extern "C" int // index of SingleObjSearch
fcore_api1_build_single(FakeEnginePtr _engine, char* builder, char* build_string)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   // =============================
   //     build_single (TESTING)
   // =============================
   std::string strBuilder{ builder };
   std::string strBuildString{ build_string };

   //
   // Example: "OptFrame:ComponentBuilder:SingleObjSearch:SA:BasicSA"
   //
   std::string sbuilder = strBuilder;
   CB* cb = engine->loader.factory.getBuilder(sbuilder);
   if (!cb) {
      std::cout << "WARNING! OptFrame builder for SingleObjSearch not found!" << std::endl;
      return -1;
   }
   //cb->buildComponent
   CBSingle* cbsingle = (CBSingle*)cb;

   //
   // Example: "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.99 100 999";
   //
   std::string scan_params = strBuildString;
   scannerpp::Scanner scanner{ scan_params };
   optframe::SingleObjSearch<FCoreLibESolution>* single = cbsingle->build(scanner, engine->loader.factory);
   std::cout << "single =" << single << std::endl;
   single->print();
   //

   optframe::Component* csingle = (optframe::Component*)single; // why??
   sptr<optframe::Component> sptrSingle{ csingle };

   int id = engine->loader.factory.addComponent(sptrSingle, "OptFrame:GlobalSearch:SingleObjSearch");
   return id;
}

extern "C" int // index of LocalSearch
fcore_api1_build_local_search(FakeEnginePtr _engine, char* builder, char* build_string)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   // =============================
   //     build_single (TESTING)
   // =============================
   std::string strBuilder{ builder };
   std::string strBuildString{ build_string };

   //
   // Example: "OptFrame:ComponentBuilder:SingleObjSearch:SA:BasicSA"
   //
   std::string sbuilder = strBuilder;
   CB* cb = engine->loader.factory.getBuilder(sbuilder);
   if (!cb) {
      std::cout << "WARNING! OptFrame builder for LocalSearch not found!" << std::endl;
      return -1;
   }
   //cb->buildComponent
   CBLocal* cblocal = (CBLocal*)cb;

   //
   // Example: "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.99 100 999";
   //
   std::string scan_params = strBuildString;
   scannerpp::Scanner scanner{ scan_params };
   optframe::LocalSearch<FCoreLibESolution>* local = cblocal->build(scanner, engine->loader.factory);
   std::cout << "local_search =" << local << std::endl;
   local->print();
   //

   optframe::Component* clocal = (optframe::Component*)local; // why??
   sptr<optframe::Component> sptrLocal{ clocal };

   int id = engine->loader.factory.addComponent(sptrLocal, "OptFrame:LocalSearch");
   return id;
}

extern "C" int // index of Component
fcore_api1_build_component(FakeEnginePtr _engine, char* builder, char* build_string, char* component_type)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   // =============================
   //     build_component
   // =============================
   std::string strBuilder{ builder };
   std::string strBuildString{ build_string };
   std::string strComponentType{ component_type };

   //
   // Example: "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2"
   //
   std::string sbuilder = strBuilder;
   CB* cb = engine->loader.factory.getBuilder(sbuilder);
   if (!cb) {
      std::cout << "WARNING! OptFrame builder '" << strBuilder << "' for Component not found!" << std::endl;
      return -1;
   }

   //
   // Example: "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:NS 0";
   //
   std::string scan_params = strBuildString;
   scannerpp::Scanner scanner{ scan_params };
   optframe::Component* c = cb->buildComponent(scanner, engine->loader.factory);
   std::cout << "component =" << c << std::endl;
   c->print();
   //
   sptr<optframe::Component> sptrComp{ c };

   int id = engine->loader.factory.addComponent(sptrComp, strComponentType);
   return id;
}

extern "C" LibSearchOutput // SearchOutput for XSH "best-type"
fcore_api1_run_sos_search(FakeEnginePtr _engine, int sos_idx, double timelimit)
{
   std::cout << "begin C++ fcore_api1_run_sos_search: sos_idx=" << sos_idx << " timelimit=" << timelimit << std::endl;
   auto* engine = (FCoreApi1Engine*)_engine;
   //
   sptr<optframe::SingleObjSearch<FCoreLibESolution>> sos;
   engine->loader.factory.assign(sos, sos_idx, "OptFrame:GlobalSearch:SingleObjSearch");
   assert(sos);
   sos->print();
   //sos->setVerbose();
   //
   optframe::SearchOutput<FCoreLibESolution> out = sos->search({ timelimit });
   std::cout << "out=" << out.status << std::endl;

   LibSearchOutput lout;
   lout.status = (int)out.status;  // ("status", c_int),
   lout.has_best = (bool)out.best; // ("has_best", ctypes.c_bool),
   if (out.best) {
      // extract pointer from solution container
      lout.best_s = out.best->first.releasePtr();  // ("best_s", ctypes.py_object),
      lout.best_e = out.best->second.evaluation(); // ("best_e", ctypes.c_double)]
   }
   return lout;
}

extern "C" bool
fcore_api1_engine_test(FakeEnginePtr _engine)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   //
   using MyEval = optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>;

   // will try to get evaluator to build InitialSolution component...
   std::shared_ptr<MyEval> ev;
   engine->loader.factory.assign(ev, 0, "OptFrame:GeneralEvaluator:Evaluator");
   assert(ev);
   sref<MyEval> ev2{ ev };
   //
   //
   using MyConstructive = optframe::Constructive<FCoreLibSolution>;
   //
   std::shared_ptr<MyConstructive> initial;
   engine->loader.factory.assign(initial, 0, "OptFrame:Constructive");
   assert(initial);
   //
   sref<optframe::InitialSearch<FCoreLibESolution>> initSol{
      new optframe::BasicInitialSearch<FCoreLibESolution>(initial, ev)
   };
   //
   std::cout << "### test will generate solution" << std::endl;
   auto ose_status = initSol->initialSearch({ 10.0 });
   std::cout << "### test will copy optional" << std::endl;
   auto ose = ose_status.first;
   std::cout << "### test will get 'se' from optional" << std::endl;
   auto se = *ose;
   std::cout << "### test will copy 'se'" << std::endl;
   auto se2 = se;

   return true;
}

extern "C" bool
fcore_api1_destroy_engine(FakeEnginePtr _engine)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   delete engine;
   // good
   return true;
}

// ==============================================
//                      ADD
// ==============================================

// min_or_max is needed to correctly cast template on FEvaluator
extern "C" int // index of generalevaluator

fcore_api1_add_float64_evaluator(FakeEnginePtr _engine,
                                 double (*_fevaluate)(FakePythonObjPtr, FakePythonObjPtr),
                                 bool min_or_max,
                                 FakePythonObjPtr problem_view)
{
   auto* engine = (FCoreApi1Engine*)_engine;
   //printf("hf=%p\n", (void*)hf);

   auto fevaluate = [_fevaluate, problem_view](const FCoreLibSolution& s) -> optframe::Evaluation<double> {
      //printf("will invoke _fevaluate(%p) over s.solution_ptr = %p\n", (void*)_fevaluate, s.solution_ptr);
      double r = _fevaluate(problem_view, s.solution_ptr);
      //printf("return r=%f\n", r);
      return r;
   };

   int id = -1;
   if (min_or_max) {
      // Minimization
      auto* ev_ptr = new optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MINIMIZE>{ fevaluate };
      sref<optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>> eval2(ev_ptr);
      sref<optframe::Component> eval(eval2);
      //std::cout << "created FEvaluator<MIN> ptr=" << &eval.get() << std::endl;
      id = engine->loader.factory.addComponent(eval, "OptFrame:GeneralEvaluator");
      // double add to prevent future down-casts
      int id2 = engine->loader.factory.addComponent(eval, "OptFrame:GeneralEvaluator:Evaluator");
      assert(id == id2);
      // also add to check module
      engine->check.addEvaluator(eval2);
   } else {
      // Maximization
      auto* ev_ptr = new optframe::FEvaluator<FCoreLibESolution, optframe::MinOrMax::MAXIMIZE>{ fevaluate };
      sref<optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>> eval2(ev_ptr);
      sref<optframe::Component> eval(eval2);

      id = engine->loader.factory.addComponent(eval, "OptFrame:GeneralEvaluator");
      // double add to prevent future down-casts
      int id2 = engine->loader.factory.addComponent(eval, "OptFrame:GeneralEvaluator:Evaluator");
      assert(id == id2);
      // also add to check module
      engine->check.addEvaluator(eval2);
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
fcore_api1_add_constructive(FakeEnginePtr _engine,
                            FakePythonObjPtr (*_fconstructive)(FakePythonObjPtr),
                            FakePythonObjPtr problem_view,
                            // Support necessary for Solution construction and maintainance
                            FakePythonObjPtr (*f_sol_deepcopy)(FakePythonObjPtr),
                            size_t (*f_sol_tostring)(FakePythonObjPtr, char*, size_t),
                            int (*f_utils_decref)(FakePythonObjPtr))
{
   auto* engine = (FCoreApi1Engine*)_engine;

   //std::cout << "invoking 'fcore_api1_add_constructive' with "
   //          << "_hf=" << _hf << " _fconstructive and problem_view=" << problem_view << std::endl;

   auto fconstructive = [_fconstructive,
                         problem_view,
                         f_sol_deepcopy,
                         f_sol_tostring,
                         f_utils_decref]() -> FCoreLibSolution {
      // IMPORTANT: _fconstructive must IncRef solution on python before returning! I think so...
      FakePythonObjPtr vobj_owned = _fconstructive(problem_view);
      //std::cout << "'fcore_api1_add_constructive' -> _fconstructive generated pointer: " << vobj_owned << std::endl;
      assert(vobj_owned); // check void* (TODO: for FxConstructive, return nullopt)
      FCoreLibSolution sol(vobj_owned, f_sol_deepcopy, f_sol_tostring, f_utils_decref);
      //std::cout << "'fcore_api1_add_constructive' -> solution created!" << std::endl;
      return sol;
   };

   auto* c_ptr = new optframe::FConstructive<FCoreLibSolution>{ fconstructive };

   sref<optframe::Constructive<FCoreLibSolution>> fc2(c_ptr);
   sref<optframe::Component> fc(fc2);

   //std::cout << "'fcore_api1_add_constructive' will add component on hf" << std::endl;

   int id = engine->loader.factory.addComponent(fc, "OptFrame:Constructive");

   //std::cout << "c_id = " << id << std::endl;
   // ========== add to check module ==========
   using MyEval = optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>;

   // will try to get evaluator to build InitialSolution component...
   std::shared_ptr<MyEval> ev;
   engine->loader.factory.assign(ev, 0, "OptFrame:GeneralEvaluator:Evaluator");
   assert(ev);
   //
   if (!ev)
      std::cout
        << "WARNING: No Evaluator! Cannot build InitialSearch for Constructive id=" << id << "!" << std::endl;
   else {
      //auto ev = std::make_shared<optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>>(
      //  gev);
      //std::shared_ptr<MyEval>
      //  ev(
      //    std::static_pointer_cast<MyEval>(gev));

      sref<optframe::InitialSearch<FCoreLibESolution>> initSol{
         new optframe::BasicInitialSearch<FCoreLibESolution>(fc2, ev)
      };
      engine->check.add(initSol);
   }
   //fc->print();
   return id;
}

extern "C" int // index of ns
fcore_api1_add_ns(FakeEnginePtr _engine,
                  FakePythonObjPtr (*_fns_rand)(FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr (*_fmove_apply)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_eq)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  bool (*_fmove_cba)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                  FakePythonObjPtr problem_view,
                  int (*_f_utils_decref)(FakePythonObjPtr))
{
   auto* engine = (FCoreApi1Engine*)_engine;

   //std::cout << "invoking 'fcore_api1_add_constructive' with "
   //          << "_hf=" << _hf << " _fconstructive and problem_view=" << problem_view << std::endl;

   // ======== preparing move functions ========
   typedef std::function<FakePythonObjPtr(const FakePythonObjPtr&, FCoreLibESolution&)> FuncTypeMoveApply;
   FuncTypeMoveApply func_fmove_apply = [_fmove_apply, problem_view](const FakePythonObjPtr& m_view, FCoreLibESolution& se) -> FakePythonObjPtr {
      // IMPORTANT: _fmove_apply must IncRef Move on python before returning! I think so...
      // m_view seems to come from Python, to be used on Python... don't know if we need to IncRef or DecRef that...
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      //
      // vobj_owned should come IncRef'ed before! I guess...
      //
      FakePythonObjPtr vobj_owned = _fmove_apply(problem_view, m_view, se.first.solution_ptr);
      // TODO: don't know if IncRef or not solution_ptr... I THINK it's a "view" for python, so no IncRef here.
      return vobj_owned;
   };

   typedef std::function<bool(const FakePythonObjPtr&, const FCoreLibESolution&)> FuncTypeMoveCBA;
   FuncTypeMoveCBA func_fmove_cba = [_fmove_cba, problem_view](const FakePythonObjPtr& m_view, const FCoreLibESolution& se) -> bool {
      // IMPORTANT: python will receive all as views..
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      bool r = _fmove_cba(problem_view, m_view, se.first.solution_ptr);
      return r;
   };

   typedef std::function<bool(const FakePythonObjPtr&, const optframe::Move<FCoreLibESolution>&)> FuncTypeMoveEq;
   FuncTypeMoveEq func_fmove_eq = [_fmove_eq, problem_view](const FakePythonObjPtr& my_m_view, const optframe::Move<FCoreLibESolution>& _mOther) -> bool {
      // cast to to lib move type. (TODO: check type... how? use OptFrame Component id()? or must improve OptFrame in this regard... not worry now!)
      auto& mOther = (FMoveLib&)_mOther;
      //
      FakePythonObjPtr mStructOtherView = mOther.m;
      // IMPORTANT: python will receive all as views..
      bool r = _fmove_eq(problem_view, my_m_view, mStructOtherView);
      return r;
   };

   typedef std::function<bool(FakePythonObjPtr)> FuncTypeUtilsDecRef;
   FuncTypeUtilsDecRef func_utils_decref = _f_utils_decref;

   //std::function<uptr<Move<XES>>(const XES&)>
   auto func_fns = [_fns_rand,
                    problem_view,
                    func_fmove_apply,
                    func_fmove_cba,
                    func_fmove_eq,
                    func_utils_decref](const FCoreLibESolution& se) -> optframe::uptr<optframe::Move<FCoreLibESolution>> {
      // IMPORTANT: _fns_rand must IncRef Move on python before returning! I think so...
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // TODO: don't know if IncRef or not solution_ptr... I THINK it's a "view" for python, so no IncRef here.
      //
      // vobj_owned should come IncRef'ed before! I guess...
      FakePythonObjPtr vobj_owned = _fns_rand(problem_view, se.first.solution_ptr);
      //std::cout << "'fcore_api1_add_ns' -> _fns_rand generated pointer: " << vobj_owned << std::endl;
      assert(vobj_owned); // check void* (TODO: allow non-existing move, return nullptr)

      //
      auto* m_ptr = new FMoveLib(vobj_owned,
                                 func_fmove_apply,
                                 func_fmove_cba,
                                 func_fmove_eq,
                                 func_utils_decref);

      //std::cout << "'fcore_api1_add_ns' -> move created!" << std::endl;
      return optframe::uptr<optframe::Move<FCoreLibESolution>>(m_ptr);
   };

   sref<optframe::NS<FCoreLibESolution>> fns(
     new optframe::FNS<FCoreLibESolution>{ func_fns });

   sref<optframe::Component> fns_comp(fns);
   //new optframe::FNS<FCoreLibESolution>{ func_fns });

   //std::cout << "'fcore_api1_add_ns' will add component on hf" << std::endl;

   int id = engine->loader.factory.addComponent(fns_comp, "OptFrame:NS");
   //
   engine->check.add(fns);
   //fns->print();
   return id;
}

// FOR NOW, WE IGNORE 'const XES' AND JUST USE 'const S'.... LET'S SEE!

extern "C" int // index of ns
fcore_api1_add_nsseq(FakeEnginePtr _engine,
                     FakePythonObjPtr (*_fns_rand)(FakePythonObjPtr, FakePythonObjPtr),
                     FakePythonObjPtr (*_fIterator)(FakePythonObjPtr, FakePythonObjPtr), // fIterator (just initializes IMS)
                     // problem*, ims*
                     void (*_fFirst)(FakePythonObjPtr, FakePythonObjPtr),               // iterator.first()
                     void (*_fNext)(FakePythonObjPtr, FakePythonObjPtr),                // iterator.next()
                     bool (*_fIsDone)(FakePythonObjPtr, FakePythonObjPtr),              // iterator.isDone()
                     FakePythonObjPtr (*_fCurrent)(FakePythonObjPtr, FakePythonObjPtr), // iterator.current()
                     FakePythonObjPtr (*_fmove_apply)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                     bool (*_fmove_eq)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                     bool (*_fmove_cba)(FakePythonObjPtr, FakePythonObjPtr, FakePythonObjPtr),
                     FakePythonObjPtr problem_view,
                     int (*_f_utils_decref)(FakePythonObjPtr))
{
   auto* engine = (FCoreApi1Engine*)_engine;

   //std::cout << "invoking 'fcore_api1_add_constructive' with "
   //          << "_hf=" << _hf << " _fconstructive and problem_view=" << problem_view << std::endl;

   // ======== preparing move functions ========
   typedef std::function<FakePythonObjPtr(const FakePythonObjPtr&, FCoreLibESolution&)> FuncTypeMoveApply;
   FuncTypeMoveApply func_fmove_apply = [_fmove_apply, problem_view](const FakePythonObjPtr& m_view, FCoreLibESolution& se) -> FakePythonObjPtr {
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // IMPORTANT: python will receive all as views..
      FakePythonObjPtr vobj_owned = _fmove_apply(problem_view, m_view, se.first.solution_ptr);
      return vobj_owned;
   };

   typedef std::function<bool(const FakePythonObjPtr&, const FCoreLibESolution&)> FuncTypeMoveCBA;
   FuncTypeMoveCBA func_fmove_cba = [_fmove_cba, problem_view](const FakePythonObjPtr& m_view, const FCoreLibESolution& se) -> bool {
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // IMPORTANT: python will receive all as views..
      bool r = _fmove_cba(problem_view, m_view, se.first.solution_ptr);
      return r;
   };

   typedef std::function<bool(const FakePythonObjPtr&, const optframe::Move<FCoreLibESolution>&)> FuncTypeMoveEq;
   FuncTypeMoveEq func_fmove_eq = [_fmove_eq, problem_view](const FakePythonObjPtr& my_m_view, const optframe::Move<FCoreLibESolution>& _mOther) -> bool {
      // cast to to lib move type. (TODO: check type... how? use OptFrame Component id()? or must improve OptFrame in this regard... not worry now!)
      auto& mOther = (FMoveLib&)_mOther;
      //
      FakePythonObjPtr mStructOtherView = mOther.m;
      // IMPORTANT: python will receive all as views..
      bool r = _fmove_eq(problem_view, my_m_view, mStructOtherView);
      return r;
   };

   typedef std::function<bool(FakePythonObjPtr)> FuncTypeUtilsDecRef;
   FuncTypeUtilsDecRef func_utils_decref = _f_utils_decref;

   //std::function<uptr<Move<XES>>(const XES&)>
   auto func_fnsrand = [_fns_rand,
                        problem_view,
                        func_fmove_apply,
                        func_fmove_cba,
                        func_fmove_eq,
                        func_utils_decref](const FCoreLibESolution& se) -> optframe::uptr<optframe::Move<FCoreLibESolution>> {
      // IMPORTANT: _fns_rand must IncRef Move on python before returning! I think so...
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // TODO: don't know if IncRef or not solution_ptr... I THINK it's a "view" for python, so no IncRef here.
      //
      // vobj_owned should come IncRef'ed before! I guess...
      FakePythonObjPtr vobj_owned = _fns_rand(problem_view, se.first.solution_ptr);
      //std::cout << "'fcore_api1_add_ns' -> _fns_rand generated pointer: " << vobj_owned << std::endl;
      assert(vobj_owned); // check void* (TODO: allow non-existing move, return nullptr)

      //
      auto* m_ptr = new FMoveLib(vobj_owned,
                                 func_fmove_apply,
                                 func_fmove_cba,
                                 func_fmove_eq,
                                 func_utils_decref);

      //std::cout << "'fcore_api1_add_ns' -> move created!" << std::endl;
      return optframe::uptr<optframe::Move<FCoreLibESolution>>(m_ptr);
   };

   // =============================
   //      Iterator Functions
   // =============================

   typedef std::function<IMSObjLib(const FCoreLibESolution&)> FuncTypeNSSeqItInit;
   // FakePythonObjPtr (*_fIterator)(FakePythonObjPtr, FakePythonObjPtr),
   FuncTypeNSSeqItInit func_fnsseq_it_init = [_fIterator, problem_view, func_utils_decref](const FCoreLibESolution& se) -> IMSObjLib {
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // IMPORTANT: python will receive all as views..
      FakePythonObjPtr ims_obj_owned = _fIterator(problem_view, se.first.solution_ptr);
      assert(ims_obj_owned);

      IMSObjLib ims{ ims_obj_owned, func_utils_decref };
      return ims;
   };

   typedef std::function<void(IMSObjLib&)> FuncTypeNSSeqItFirst;
   // void (*_fFirst)(FakePythonObjPtr, FakePythonObjPtr),
   FuncTypeNSSeqItFirst func_fnsseq_it_first = [_fFirst, problem_view](IMSObjLib& it) -> void {
      // IMPORTANT: python will receive all as views..
      _fFirst(problem_view, it.ims_ptr);
   };

   typedef std::function<void(IMSObjLib&)> FuncTypeNSSeqItNext;
   // void (*_fFirst)(FakePythonObjPtr, FakePythonObjPtr),
   FuncTypeNSSeqItNext func_fnsseq_it_next = [_fNext, problem_view](IMSObjLib& it) -> void {
      // IMPORTANT: python will receive all as views..
      _fNext(problem_view, it.ims_ptr);
   };

   typedef std::function<bool(IMSObjLib&)> FuncTypeNSSeqItIsDone;

   FuncTypeNSSeqItIsDone func_fnsseq_it_isdone = [_fIsDone, problem_view](IMSObjLib& it) -> bool {
      // IMPORTANT: python will receive all as views..
      bool b = _fIsDone(problem_view, it.ims_ptr);
      return b;
   };

   typedef std::function<optframe::uptr<optframe::Move<FCoreLibESolution>>(IMSObjLib & it)> FuncTypeNSSeqItCurrent;

   FuncTypeNSSeqItCurrent func_fnsseq_it_current = [_fCurrent,
                                                    problem_view,
                                                    func_fmove_apply,
                                                    func_fmove_cba,
                                                    func_fmove_eq,
                                                    func_utils_decref](IMSObjLib& it) -> optframe::uptr<optframe::Move<FCoreLibESolution>> {
      // TODO: will pass ESolution as a Solution in API1... ignoring Evaluation/Re-evaluation!
      // IMPORTANT: python will receive all as views..
      FakePythonObjPtr vobj_owned = _fCurrent(problem_view, it.ims_ptr);
      assert(vobj_owned); // check void* (TODO: allow non-existing move, return nullptr)

      //
      auto* m_ptr = new FMoveLib(vobj_owned,
                                 func_fmove_apply,
                                 func_fmove_cba,
                                 func_fmove_eq,
                                 func_utils_decref);

      //std::cout << "'fcore_api1_add_ns' -> move created!" << std::endl;
      return optframe::uptr<optframe::Move<FCoreLibESolution>>(m_ptr);
   };
   /*
      FNSSeq(
     uptr<Move<XES>> (*_fRandom)(const XES&), // fRandom
     IMS (*_fIterator)(const XES&),           // fIterator (just initializes IMS)
     void (*_fFirst)(IMS&),                   // iterator.first()
     void (*_fNext)(IMS&),                    // iterator.next()
     bool (*_fIsDone)(IMS&),                  // iterator.isDone()
     uptr<Move<XES>> (*_fCurrent)(IMS&)       // iterator.current()
     )
   */

   sref<optframe::NSSeq<FCoreLibESolution>>
     fnsseq(new optframe::FNSSeq<IMSObjLib, FCoreLibESolution>{ func_fnsrand,
                                                                func_fnsseq_it_init,
                                                                func_fnsseq_it_first,
                                                                func_fnsseq_it_next,
                                                                func_fnsseq_it_isdone,
                                                                func_fnsseq_it_current });

   sref<optframe::Component> fnsseq_comp(fnsseq);

   //std::cout << "'fcore_api1_add_nsseq' will add component on hf" << std::endl;

   int id = engine->loader.factory.addComponent(fnsseq_comp, "OptFrame:NS:NSFind:NSSeq");
   //
   engine->check.add(fnsseq);
   //fns->print();
   return id;
}

extern "C" int // index of InitialSearch
fcore_api1_create_initial_search(FakeEnginePtr _engine, int ev_idx, int c_idx)
{
   auto* engine = (FCoreApi1Engine*)_engine;

   using MyEval = optframe::Evaluator<FCoreLibSolution, optframe::Evaluation<double>, FCoreLibESolution>;

   // will try to get evaluator to build InitialSolution component...
   std::shared_ptr<MyEval> _ev;
   engine->loader.factory.assign(_ev, ev_idx, "OptFrame:GeneralEvaluator:Evaluator");
   assert(_ev);
   sref<MyEval> single_ev{ _ev };
   //
   //
   using MyConstructive = optframe::Constructive<FCoreLibSolution>;
   //
   std::shared_ptr<MyConstructive> initial;
   engine->loader.factory.assign(initial, c_idx, "OptFrame:Constructive");
   assert(initial);
   //
   sref<optframe::InitialSearch<FCoreLibESolution>> initSol{
      new optframe::BasicInitialSearch<FCoreLibESolution>(initial, single_ev)
   };

   int id = engine->loader.factory.addComponent(initSol, "OptFrame:InitialSearch");
   //
   //engine->check.add(fns);

   return id;
}

// ==============================================
//                      GET
// ==============================================

extern "C" void* // raw (non-owned) pointer to GeneralEvaluator
fcore_api1_get_float64_evaluator(FakeEnginePtr _engine, int idx_ev)
{
   auto* engine = (FCoreApi1Engine*)_engine;

   std::shared_ptr<optframe::GeneralEvaluator<FCoreLibESolution, FCoreLibESolution::second_type>> component;

   engine->loader.factory.assign(component, idx_ev, "OptFrame:GeneralEvaluator");
   if (!component)
      assert(false);
   void* ptr = component.get();
   return ptr;
}

extern "C" void* // raw (non-owned) pointer to FConstructive
fcore_api1_get_constructive(FakeEnginePtr _engine, int idx_c)
{
   auto* engine = (FCoreApi1Engine*)_engine;

   std::shared_ptr<optframe::Constructive<FCoreLibSolution>> component;

   engine->loader.factory.assign(component, idx_c, "OptFrame:Constructive");
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

// RAW METHOD (SHOULD WE KEEP IT?)
extern "C" void
fcore_raw_component_print(void* component)
{
   auto* c = (optframe::Component*)component;
   //std::cout << "fcore_component_print ptr=" << c << " => ";
   c->print();
}

extern "C" bool
fcore_api1_engine_component_set_loglevel(FakeEnginePtr _engine, char* _scomponent, int loglevel, bool recursive)
{
   auto* engine = (FCoreApi1Engine*)_engine;

   std::string scomponent{ _scomponent };
   scannerpp::Scanner scanner{ scomponent };

   sptr<optframe::Component> c = engine->loader.factory.getNextComponent(scanner);

   if (!c)
      return false;

   assert(loglevel >= 0);
   assert(loglevel <= 5);

   /*
   enum LogLevel
   {
      Silent = 0,
      Error = 1,
      Warning = 2,
      Info = 3, (DEFAULT)
      Debug = 4
   };
   */

   auto ll = (optframe::LogLevel)loglevel;

   assert(!recursive); // TODO: Must create 'setMessageLevelR'

   c->setMessageLevel(ll);

   return true;
}

// ==============================================