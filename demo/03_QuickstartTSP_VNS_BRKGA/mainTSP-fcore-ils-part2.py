
# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')
print(pTSP)

# Register Basic Components
comp_list = pTSP.engine.setup(pTSP)
print(comp_list)

# get index of new NS
ns_idx = pTSP.engine.add_ns_class(pTSP, NSSwap)
print("ns_idx=", ns_idx)

# get index of new NSSeq
nsseq_idx = pTSP.engine.add_nsseq_class(pTSP, NSSeqSwap)
print("nsseq_idx=", nsseq_idx)

# ========= play a little bit =========

gev_idx = comp_list[0] # GeneralEvaluator
ev_idx  = comp_list[1] # Evaluator
print("evaluator id:", ev_idx)

c_idx = comp_list[2]
print("c_idx=", c_idx)

is_idx = IdInitialSearch(0)
print("is_idx=", is_idx)

# test each component

fev = pTSP.engine.get_evaluator(ev_idx)
pTSP.engine.print_component(fev)

fc = pTSP.engine.get_constructive(c_idx)
pTSP.engine.print_component(fc)

solxx = pTSP.engine.fconstructive_gensolution(fc)
print("test solution:", solxx)

z1 = pTSP.engine.fevaluator_evaluate(fev, True, solxx)
print("test evaluation:", z1)

# some basic tests with moves and iterator
move = MoveSwapClass(0,1) # swap 0 with 1
print("move=",move)
m1 = NSSwap.randomMove(pTSP, solxx)
print(m1)

print("begin test with iterator")
it = NSSeqSwap.getIterator(pTSP, solxx)
it.first(pTSP)
while not it.isDone(pTSP):
    m = it.current(pTSP)
    print(m)
    it.next(pTSP)
print("end test with iterator")

# ======== end playing ========

# pack NS into a NS list
list_idx = pTSP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
print("list_idx=", list_idx)

# print("Listing registered components:")
# pTSP.engine.list_components("OptFrame:")

# list the required parameters for OptFrame ComponentBuilder
# print("engine will list builders for OptFrame: ")
# print(pTSP.engine.list_builders("OptFrame:"))
# print()

# make next local search component silent (loglevel 0)
pTSP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

print("building 'BI' neighborhood exploration as local search", flush=True)
bi = BestImprovement(pTSP.engine, 0, 0)
ls_idx = bi.get_id()
print("ls_idx=", ls_idx, flush=True)

print("creating local search list", flush=True)
list_vnd_idx = pTSP.engine.create_component_list(
    "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")
print("list_vnd_idx=", list_vnd_idx)


print("building 'VND' local search")
vnd = VariableNeighborhoodDescent(pTSP.engine, 0, 0)
vnd_idx = vnd.get_id()
print("vnd_idx=", vnd_idx)
