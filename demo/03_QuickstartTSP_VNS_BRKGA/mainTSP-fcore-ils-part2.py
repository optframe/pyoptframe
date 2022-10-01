
# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')
#pTSP.n  = 5
#pTSP.vx = [10, 20, 30, 40, 50]
#pTSP.vy = [10, 20, 30, 40, 50]
#pTSP.dist = ...

# initializes optframe engine
pTSP.engine = optframe.Engine(optframe.APILevel.API1d)
print(pTSP)

# Register Basic Components

ev_idx = pTSP.engine.minimize(pTSP, mycallback_fevaluate)
print("evaluator id:", ev_idx)

c_idx = pTSP.engine.add_constructive(pTSP, mycallback_constructive)
print("c_idx=", c_idx)

is_idx = pTSP.engine.create_initial_search(ev_idx, c_idx)
print("is_idx=", is_idx)

# test each component

fev = pTSP.engine.get_evaluator(ev_idx)
pTSP.engine.print_component(fev)

fc = pTSP.engine.get_constructive(c_idx)
pTSP.engine.print_component(fc)

solxx = pTSP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z1 = pTSP.engine.fevaluator_evaluate(fev, False, solxx)
print("evaluation:", z1)


# list the required parameters for OptFrame ComponentBuilder
print("engine will list builders for OptFrame: ")
print(pTSP.engine.list_builders("OptFrame:"))
print()

# get index of new NS
ns_idx = pTSP.engine.add_ns(pTSP,
                           mycallback_ns_rand_swap,
                           apply_swap,
                           eq_swap,
                           cba_swap)
print("ns_idx=", ns_idx)

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
