
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

c_rk_idx = pTSP.engine.add_constructive_rk(pTSP, mycallback_constructive_rk)
print("c_rk_idx=", c_rk_idx)

pTSP.engine.list_components("OptFrame:")

initepop_rk_id = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicInitialEPopulationRKBuilder", 
    "OptFrame:Constructive:EA:RK:ConstructiveRK 0",
    "OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK")
print("initepop_rk_id=", initepop_rk_id)

print("")
print("WILL CREATE DECODER!!")
dec_rk_idx = pTSP.engine.add_decoder_rk(pTSP, mycallback_decoder_rk)
print("dec_rk_idx=", dec_rk_idx)

pTSP.engine.list_components("OptFrame:")

print("")
print("WILL BUILD COMPLETE DECODER WITH EVALUATOR!!")
drk_rk_id = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:EA:RK:BasicDecoderRandomKeysBuilder", 
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:EA:RK:DecoderRandomKeysNoEvaluation 0",
    "OptFrame:EA:RK:DecoderRandomKeys")
print("drk_rk_id=", drk_rk_id)


# =======================

print("")
print("testing builder (build_global_search) for BRKGA...")
print("")

g_idx = pTSP.engine.build_global_search(
    "OptFrame:ComponentBuilder:GlobalSearch:EA:RK:BRKGA",
    "OptFrame:EA:RK:DecoderRandomKeys 0  OptFrame:InitialEPopulation:EA:RK:InitialEPopulationRK 0 "
    "30 1000 0.4 0.3 0.6")
print("g_idx=", g_idx)



pTSP.engine.list_components("OptFrame:")

print("")
print("testing execution of GlobalSearch (run_global_search) for BRKGA...")
print("")

lout = pTSP.engine.run_global_search(g_idx, 3.0)
print('solution:', lout)

print("FINISHED")
