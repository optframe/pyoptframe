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
#       Helper Components
# ================================

class ILSLevelPertLPlus2(object):
    def __init__(self, _engine: XEngine, _ev: IdGeneralEvaluator, _ns: IdNS):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdGeneralEvaluator(_ev)
        if (not isinstance(_ev, IdGeneralEvaluator)):
            print(_ev)
            assert (False)
        if (isinstance(_ns, int)):
            _ns = IdNS(_ns)
        if (not isinstance(_ns, IdNS)):
            print(_ns)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2"
        str_args    = "OptFrame:GeneralEvaluator "+str(_ev.id)+" OptFrame:NS "+str(_ns.id)
        str_target  = "OptFrame:ILS:LevelPert"
        self.comp_idx  = IdILSLevelPert(self.engine.build_component(str_code, str_args, str_target))
    def get_id(self) -> IdILSLevelPert:
        return self.comp_idx



class DecoderRandomKeys(object):
    def __init__(self, _engine: XEngine, _ev: IdEvaluator, _decoder: IdDecoderRandomKeysNoEvaluation):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdEvaluator(_ev)
        if (not isinstance(_ev, IdEvaluator)):
            print(_ev)
            assert (False)
        if (isinstance(_decoder, int)):
            _decoder = IdDecoderRandomKeysNoEvaluation(_decoder)
        if (not isinstance(_decoder, IdDecoderRandomKeysNoEvaluation)):
            print(_decoder)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:EA:RK:BasicDecoderRandomKeysBuilder"
        str_args    = "OptFrame:GeneralEvaluator:Evaluator "+str(_ev.id)+" OptFrame:EA:RK:DecoderRandomKeysNoEvaluation "+str(_decoder.id)
        str_target  = "OptFrame:EA:RK:DecoderRandomKeys"
        self.comp_idx  = IdDecoderRandomKeys(self.engine.build_component(str_code, str_args, str_target))
    def get_id(self) -> IdDecoderRandomKeys:
        return self.comp_idx


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
        str_args    = "OptFrame:GeneralEvaluator "+str(_ev.id)+" OptFrame:NS:NSFind:NSSeq "+str(_nsseq.id)
        self.ls_idx  = self.engine.build_local_search(str_code, str_args)
    def get_id(self) -> IdLocalSearch:
        return self.ls_idx

class VariableNeighborhoodDescent(LocalSearch):
    def __init__(self, _engine: XEngine, _ev: IdGeneralEvaluator, _lslist: IdListLocalSearch):
        assert isinstance(_engine, XEngine)
        if (isinstance(_ev, int)):
            _ev = IdGeneralEvaluator(_ev)
        if (not isinstance(_ev, IdGeneralEvaluator)):
            print(_ev)
            assert (False)
        if (isinstance(_lslist, int)):
            _lslist = IdListLocalSearch(_lslist)
        if (not isinstance(_lslist, IdListLocalSearch)):
            print(_lslist)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:LocalSearch:VND"
        str_args    = "OptFrame:GeneralEvaluator "+str(_ev.id)+" OptFrame:LocalSearch[] "+str(_lslist.id)
        self.ls_idx  = self.engine.build_local_search(str_code, str_args)
    def get_id(self) -> IdLocalSearch:
        return self.ls_idx


class BRKGA(SingleObjSearch):
    def __init__(self, _engine: XEngine, _decoder: IdDecoderRandomKeys, _init_rk: IdInitialEPopulationRK, popSize: int, numGen: int, fracTop: float, fracBOT:float, probElitism: float):
        assert isinstance(_engine, XEngine)
        if (isinstance(_decoder, int)):
            _decoder = IdDecoderRandomKeys(_decoder)
        if (not isinstance(_decoder, IdDecoderRandomKeys)):
            print(_decoder)
            assert (False)
        if (isinstance(_init_rk, int)):
            _init_rk = IdInitialEPopulationRK(_init_rk)
        if (isinstance(_init_rk, IdConstructiveRK)):
            print("WARNING: will create InitialEPopulationRK")
            initepop_rk_id = _engine.build_component(
                "OptFrame:ComponentBuilder:EA:RK:BasicInitialEPopulationRKBuilder", 
                "OptFrame:Constructive<XRKf64>:EA:RK:ConstructiveRK "+str(_init_rk.id),
                "OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK")
            # print("initepop_rk_id=", initepop_rk_id)
            _init_rk = IdInitialEPopulationRK(initepop_rk_id)
        if (not isinstance(_init_rk, IdInitialEPopulationRK)):
            print(_init_rk)
            assert (False)
        self.engine = _engine
        str_code    = "OptFrame:ComponentBuilder:GlobalSearch:EA:RK:BRKGA"
        str_args    = "OptFrame:EA:RK:DecoderRandomKeys "+str(_decoder.id)+" OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK "+str(_init_rk.id)+" "+str(popSize)+" "+str(numGen)+" "+str(fracTop)+" "+ str(fracBOT)+ " "+ str(probElitism)
        self.g_idx  = self.engine.build_global_search(str_code, str_args)
    def search(self, timelimit: float) -> SearchOutput:
        lout : SearchOutput = self.engine.run_global_search(self.g_idx, timelimit)
        return lout


