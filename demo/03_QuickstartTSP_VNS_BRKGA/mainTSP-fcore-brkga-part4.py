

# set random seed for system
random.seed(0) # bad generator, just an example..

# loads problem from filesystem
pTSP = ProblemContextTSP()
pTSP.load('tsp-example.txt')

print("problem=",pTSP)

import optframe
print(str(optframe.__version__))
pTSP.engine.welcome()


# Register Basic Components
comp_list = pTSP.engine.setup(pTSP)
print(comp_list)
#
ev_idx = comp_list[1]
print("evaluator id:", ev_idx)

c_rk_idx = pTSP.engine.add_constructive_rk_class(pTSP, RKConstructiveTSP)
print("c_rk_idx=", c_rk_idx)

print("")
dec_rk_idx = pTSP.engine.add_decoder_rk_class(pTSP, DecoderTSP)
print("dec_rk_idx=", dec_rk_idx)

print("")
print("WILL CREATE DecoderRandomKeys directly with simultaneous evaluation and optional solution!")
drk_rk_id = pTSP.engine.add_edecoder_op_rk_class(pTSP, DecoderTSP)
print("drk_rk_id=", drk_rk_id)

pTSP.engine.list_components("OptFrame:")

#print("")
#print("WILL CREATE DecoderRandomKeys FROM DecoderRandomKeysNoEvaluation!")
#drk = DecoderRandomKeys(pTSP.engine, ev_idx, dec_rk_idx)
#drk_rk_id = drk.get_id()
#print("drk_rk_id=", drk_rk_id)

# =======================
# pTSP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "4")
print("")
print("will start BRKGA for 3 seconds")
brkga = BRKGA(pTSP.engine, drk_rk_id, c_rk_idx, 30, 1000, 0.4, 0.3, 0.6)

pTSP.engine.list_components("OptFrame:")

lout = brkga.search(3.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)

