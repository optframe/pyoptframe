
# set random seed for system
# random.seed(10)

# loads problem from filesystem
pKP = ProblemContextKP()
pKP.load('knapsack-example.txt')
#pKP.n = 5
#pKP.w = [1, 2, 3, 7, 8]
#pKP.p = [1, 1, 1, 5, 5]
#pKP.Q = 10.0

# initializes optframe engine
pKP.engine = optframe.Engine(optframe.APILevel.API1d)
print(pKP)

# make engine silent (loglevel 0)
pKP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "0")
