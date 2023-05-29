
# list the required parameters for OptFrame SA ComponentBuilder
print("engine will list builders for :BasicSA ")
print(pKP.engine.list_builders(":BasicSA"))
print()

# get index of new NS
ns_idx = pKP.engine.add_ns(pKP,
                           mycallback_ns_rand_bitflip,
                           apply_bitflip,
                           eq_bitflip,
                           cba_bitflip)
print("ns_idx=", ns_idx)

# pack NS into a NS list
list_idx = pKP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)

# make global search silent (loglevel 0)
pKP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
gs_idx = pKP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.98 100 99999")
print("gs_idx=", gs_idx)

# run Simulated Annealing for 10.0 seconds
lout = pKP.engine.run_global_search(gs_idx, 10.0)
print('lout=', lout)