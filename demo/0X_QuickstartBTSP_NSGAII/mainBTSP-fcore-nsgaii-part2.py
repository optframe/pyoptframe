
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

c_idx = pBTSP.engine.add_constructive(pBTSP, mycallback_constructive)
print("c_idx=", c_idx)


# test each component

fev0 = pBTSP.engine.get_evaluator(ev0_idx)
pBTSP.engine.print_component(fev0)

fev1 = pBTSP.engine.get_evaluator(ev1_idx)
pBTSP.engine.print_component(fev1)

fc = pBTSP.engine.get_constructive(c_idx)
pBTSP.engine.print_component(fc)

solxx = pBTSP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z0 = pBTSP.engine.fevaluator_evaluate(fev0, False, solxx)
print("evaluation obj 0:", z0)

z1 = pBTSP.engine.fevaluator_evaluate(fev1, False, solxx)
print("evaluation obj 1:", z1)

# pack Evaluator's into a Evaluator list
list_ev_idx = pBTSP.engine.create_component_list(
    "[ OptFrame:GeneralEvaluator:Evaluator 0 "
    " OptFrame:GeneralEvaluator:Evaluator 1 ]", 
    "OptFrame:GeneralEvaluator:Evaluator[]")
print("list_ev_idx=", list_ev_idx)

#####

print("engine will list builders for :MultiEvaluator")
print("count=", pBTSP.engine.list_builders(":MultiEvaluator"))
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
print(pBTSP.engine.list_builders("OptFrame:"))
print()

# get index of new NS
ns_idx = pBTSP.engine.add_ns(pBTSP,
                           mycallback_ns_rand_swap,
                           apply_swap,
                           eq_swap,
                           cba_swap,
                           True) # This is XMES (Multi Objective)
print("ns_idx=", ns_idx)

####
pBTSP.engine.list_components("OptFrame:")
####

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
