

#####
#pTSP.engine.list_components("OptFrame:")

ilsl_pert = ILSLevelPertLPlus2(pTSP.engine, 0, 0)
pert_idx = ilsl_pert.get_id()
print("pert_idx=", pert_idx)

# pTSP.engine.list_components("OptFrame:")

# make next global search component info (loglevel 3)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "3")

# build Iterated Local Search (ILS) Levels with iterMax=10 maxPert=5
ilsl = ILSLevels(pTSP.engine, 0, 0, 1, 0, 10, 5)
print("will start ILS for 3 seconds")
lout = ilsl.search(3.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)

print("FINISHED")
