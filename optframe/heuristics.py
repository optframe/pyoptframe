#!/usr/bin/python3

from optframe.protocols import *
from optframe.components import *

class BasicSimulatedAnnealing(SingleObjSearch):
    def __init__(self, _engine: XEngine, _ev: IdGeneralEvaluator, _is: IdInitialSearch, _lns: IdListNS, alpha:float, iter:int, T0:float):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdGeneralEvaluator(_ev)
        if (not isinstance(_ev, IdGeneralEvaluator)):
            print(_ev)
            assert (False)
        if (isinstance(_is, int)):
            _is = IdInitialSearch(_is)
        if (not isinstance(_is, IdInitialSearch)):
            print(_is)
            assert (False)
        if (not isinstance(_lns, IdListNS)):
            print(_lns)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA"
        str_args    = "OptFrame:GeneralEvaluator:Evaluator "+str(_ev.id)+" OptFrame:InitialSearch "+str(_is.id)+" OptFrame:NS[] "+str(_lns.id)+" "+str(alpha)+" "+str(iter)+" "+str(T0)
        self.g_idx  = self.engine.build_global_search(str_code, str_args)
    def search(self, timelimit: float) -> SearchOutput:
        lout : SearchOutput = self.engine.run_global_search(self.g_idx, timelimit)
        return lout


class ILSLevels(SingleObjSearch):
    def __init__(self, _engine: XEngine, _ev: IdGeneralEvaluator, _is: IdInitialSearch, _ls: IdLocalSearch, _ilslpert: IdILSLevelPert, iterMax:int, maxPert:int):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdGeneralEvaluator(_ev)
        if (not isinstance(_ev, IdGeneralEvaluator)):
            assert (False)
        if (isinstance(_is, int)):
            _is = IdInitialSearch(_is)
        if (not isinstance(_is, IdInitialSearch)):
            assert (False)
        if (isinstance(_ls, int)):
            _ls = IdLocalSearch(_ls)
        if (not isinstance(_ls, IdLocalSearch)):
            assert (False)
        if (isinstance(_ilslpert, int)):
            _ilslpert = IdILSLevelPert(_ilslpert)
        if (not isinstance(_ilslpert, IdILSLevelPert)):
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels"
        str_args    = "OptFrame:GeneralEvaluator:Evaluator "+str(_ev.id)+" OptFrame:InitialSearch "+str(_is.id)+" OptFrame:LocalSearch "+str(_ls.id)+" OptFrame:ILS:LevelPert "+str(_ilslpert.id)+" "+str(iterMax)+" "+str(maxPert)
        self.g_idx  = self.engine.build_global_search(str_code, str_args)
    def search(self, timelimit: float) -> SearchOutput:
        lout : SearchOutput = self.engine.run_global_search(self.g_idx, timelimit)
        return lout


# ================================
#         Local Search
# ================================

class BestImprovement(LocalSearch):
    def __init__(self, _engine: XEngine, _ev: IdGeneralEvaluator, _nsseq: IdNSSeq):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdGeneralEvaluator(_ev)
        if (not isinstance(_ev, IdGeneralEvaluator)):
            print(_ev)
            assert (False)
        if (isinstance(_nsseq, int)):
            _nsseq = IdNSSeq(_nsseq)
        if (not isinstance(_nsseq, IdNSSeq)):
            print(_nsseq)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:LocalSearch:BI"
        str_args    = "OptFrame:GeneralEvaluator:Evaluator "+str(_ev.id)+" OptFrame:NS:NSFind:NSSeq "+str(_nsseq.id)
        self.ls_idx  = self.engine.build_local_search(str_code, str_args)
    
