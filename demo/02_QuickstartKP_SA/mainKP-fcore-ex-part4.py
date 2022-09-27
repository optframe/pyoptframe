
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

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
sos_idx = pKP.engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:SA:BasicSA",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.98 100 99999")
print("sos_idx=", sos_idx)

# run Simulated Annealing for 10.0 seconds
lout = pKP.engine.run_sos_search(sos_idx, 10.0)
print('lout=', lout)