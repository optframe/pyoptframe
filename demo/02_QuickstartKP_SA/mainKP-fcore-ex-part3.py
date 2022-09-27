
ev_idx = pKP.engine.maximize(pKP, mycallback_fevaluate)
print("evaluator id:", ev_idx)

c_idx = pKP.engine.add_constructive(pKP, mycallback_constructive)
print("c_idx=", c_idx)

is_idx = pKP.engine.create_initial_search(ev_idx, c_idx)
print("is_idx=", is_idx)

# test each component

fev = pKP.engine.get_evaluator(ev_idx)
pKP.engine.print_component(fev)

fc = pKP.engine.get_constructive(c_idx)
pKP.engine.print_component(fc)

solxx = pKP.engine.fconstructive_gensolution(fc)
print("solxx:", solxx)

z1 = pKP.engine.fevaluator_evaluate(fev, False, solxx)
print("evaluation:", z1)
