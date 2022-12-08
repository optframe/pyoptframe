
# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pBTSP = ProblemContextBTSP()
pBTSP.load('btsp-example.txt')
#pBTSP.n  = 5


# initializes optframe engine
pBTSP.engine = optframe.Engine(optframe.APILevel.API1d)
print(pBTSP)

# Register Basic Components

ev0_idx = pBTSP.engine.minimize(pBTSP, mycallback_fevaluate0)
print("evaluator id:", ev0_idx)

ev1_idx = pBTSP.engine.minimize(pBTSP, mycallback_fevaluate1)
print("evaluator id:", ev1_idx)

ev2_idx = pBTSP.engine.minimize(pBTSP, mycallback_fevaluate2)
print("evaluator id:", ev2_idx)

c_idx = pBTSP.engine.add_constructive(pBTSP, mycallback_constructive)
print("c_idx=", c_idx)


# test each component

fev0 = pBTSP.engine.get_evaluator(ev0_idx)
pBTSP.engine.print_component(fev0)

fev1 = pBTSP.engine.get_evaluator(ev1_idx)
pBTSP.engine.print_component(fev1)

fev2 = pBTSP.engine.get_evaluator(ev2_idx)
pBTSP.engine.print_component(fev2)

fc = pBTSP.engine.get_constructive(c_idx)
pBTSP.engine.print_component(fc)

solxx = pBTSP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z0 = pBTSP.engine.fevaluator_evaluate(fev0, False, solxx)
print("evaluation obj 0:", z0)

z1 = pBTSP.engine.fevaluator_evaluate(fev1, False, solxx)
print("evaluation obj 1:", z1)

z2 = pBTSP.engine.fevaluator_evaluate(fev2, False, solxx)
print("evaluation obj 2:", z2)

print("   = = = Will PACK both Evaluators in a MultiEvaluator")
# pack Evaluator's into a Evaluator list
list_ev_idx = pBTSP.engine.create_component_list(
    "[ OptFrame:GeneralEvaluator:Evaluator 0 , OptFrame:GeneralEvaluator:Evaluator 1 , OptFrame:GeneralEvaluator:Evaluator 2 ]", 
    "OptFrame:GeneralEvaluator:Evaluator[]")
print("list_ev_idx=", list_ev_idx)

#####

print("engine will list builders for :MultiEvaluator")
#print("count=", pBTSP.engine.list_builders(":MultiEvaluator"))
print()

mev_idx = pBTSP.engine.build_component(
    "OptFrame:ComponentBuilder:MultiEvaluator",
    "OptFrame:GeneralEvaluator:Evaluator[] 0",
    "OptFrame:GeneralEvaluator:MultiEvaluator")
print("mev_idx=", mev_idx)

cross_idx = pBTSP.engine.add_crossover(pBTSP, mycallback_cross1, mycallback_cross2)
print("cross_idx=", cross_idx)

####
pBTSP.engine.list_components("OptFrame:")
####

pop_init_idx = pBTSP.engine.build_component(
    "OptFrame:ComponentBuilder:BasicInitialMultiESolution",
    "OptFrame:Constructive 0  OptFrame:GeneralEvaluator:MultiEvaluator 0",
    "OptFrame:InitialMultiESolution:BasicInitialMultiESolution")
print("pop_init_idx=", pop_init_idx)



# list the required parameters for OptFrame ComponentBuilder
print("engine will list builders for OptFrame: ")
# print(pBTSP.engine.list_builders("OptFrame:"))
print()

# get index of new NS
ns_idx = pBTSP.engine.add_ns(pBTSP,
                           mycallback_ns_rand_swap,
                           apply_swap,
                           eq_swap,
                           cba_swap,
                           True) # This is XMES (Multi Objective)
print("ns_idx=", ns_idx)

# pack NS<XMESf64>'s into a NS<XMESf64> list
list_ns_mev_idx = pBTSP.engine.create_component_list(
    "[ OptFrame:NS<XMESf64> 0 ]", 
    "OptFrame:NS<XMESf64>[]")
print("list_ns_mev_idx=", list_ns_mev_idx)

# pack OptFrame:GeneralCrossover
list_cross_idx = pBTSP.engine.create_component_list(
    "[ OptFrame:GeneralCrossover 0 ]", 
    "OptFrame:GeneralCrossover[]")
print("list_cross_idx=", list_cross_idx)


####
pBTSP.engine.list_components("OptFrame:")
####

mopop_manage_idx = pBTSP.engine.build_component(
    "OptFrame:ComponentBuilder:BasicMOPopulationManagement",
    "OptFrame:InitialMultiESolution:BasicInitialMultiESolution 0 "
    "OptFrame:NS<XMESf64>[] 0  0.5  OptFrame:GeneralCrossover[] 0  0.1",
    "OptFrame:MOPopulationManagement")
print("mopop_manage_idx=", mopop_manage_idx)

#builder: OptFrame:ComponentBuilder:BasicMOPopulationManagementBuilder |params|=5
#	param 0 => OptFrame:InitialMultiESolution : initial epopulation
#	param 1 => OptFrame:NS<XMESf64>[] : list of NS
#	param 2 => OptFrame:double : mutation rate
#	param 3 => OptFrame:GeneralCrossover[] : list of crossover
#	param 4 => OptFrame:double : renew rate

st=pBTSP.engine.run_nsgaii_params(10.0, 0, 100000, 0, 0, 30, 100)
print(st)

exit(1)

# pack NS into a NS list
list_idx = pTSP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)


# get index of new NSSeq
nsseq_idx = pTSP.engine.add_nsseq(pTSP,
                                 mycallback_ns_rand_swap,
                                 mycallback_nsseq_it_init_swap,
                                 mycallback_nsseq_it_first_swap,
                                 mycallback_nsseq_it_next_swap,
                                 mycallback_nsseq_it_isdone_swap,
                                 mycallback_nsseq_it_current_swap,
                                 apply_swap,
                                 eq_swap,
                                 cba_swap)
print("nsseq_idx=", nsseq_idx)


print("building 'BI' neighborhood exploration as local search")

ls_idx = pTSP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:BI",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS:NSFind:NSSeq 0")
print("ls_idx=", ls_idx)


print("creating local search list")

list_vnd_idx = pTSP.engine.create_component_list(
    "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")
print("list_vnd_idx=", list_vnd_idx)


print("building 'VND' local search")

vnd_idx = pTSP.engine.build_local_search(
    "OptFrame:ComponentBuilder:LocalSearch:VND",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:LocalSearch[] 0")
print("vnd_idx=", vnd_idx)
