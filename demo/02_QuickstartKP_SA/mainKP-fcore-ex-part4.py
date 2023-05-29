
# list the required parameters for OptFrame SA ComponentBuilder
print("engine will list builders for :BasicSA ")
print(pKP.engine.list_builders(":BasicSA"))
print()

# register NS class
pKP.engine.add_ns_class(pKP, NSBitFlip) 
ns_idx = 0

# pack NS into a NS list
list_idx = pKP.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")


# make global search silent (loglevel 0)
pKP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

# check components!
pKP.engine.check(100, 10, False)

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
sa = BasicSimulatedAnnealing(pKP.engine, 0, 0, list_idx, 0.98, 100, 99999)
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)
