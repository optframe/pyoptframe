

#####
pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_component) for ILSLevels...")
print("")

pert_idx = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")
print("pert_idx=", pert_idx)

pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_single_obj_search) for ILS...")
print("")

# make next global search component info (loglevel 3)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "3")

#sos_idx = pTSP.engine.build_single_obj_search(
#    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
#    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 1 OptFrame:ILS:LevelPert 0  10  5")
#print("sos_idx=", sos_idx)

print("will start ILS for 3 seconds")

#lout = pTSP.engine.run_sos_search(sos_idx, 3.0) # 3.0 seconds max
#print('lout=', lout)

# build ILS Levels with iterMax=10 maxPert=5
ilsl = ILSLevels(pTSP.engine, 0, 0, 1, 0, 10, 5)
lout = ilsl.search(3.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)


print("FINISHED")
