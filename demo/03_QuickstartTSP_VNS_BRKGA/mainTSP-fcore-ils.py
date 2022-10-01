# OptFrame Python Demo TSP - Traveling Salesman Problem

import optframe

class SolutionTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n = 0
        # visited cities as a list
        self.cities = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionTSP(n={self.n};cities={self.cities})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo):
        sol2 = SolutionTSP()
        sol2.n = self.n
        sol2.cities = [i for i in self.cities]
        return sol2

    def __del__(self):
        # print("~SolutionTSP")
        pass
import math

class ProblemContextTSP(object):
    def __init__(self):
        print('Init TSP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of cities
        self.n = 0
        # x coordinates
        self.vx = []
        # y coordinates
        self.vy = []
        # distance matrix
        self.dist = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx.append(int(id_x_y[1]))
               self.vy.append(int(id_x_y[2]))
            #
            self.dist = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist[i][j] = round(self.euclidean(self.vx[i], self.vy[i], self.vx[j], self.vy[j]))

    def euclidean(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextTSP(n={self.n};vx={self.vx};vy={self.vy};dist={self.dist})"

def mycallback_fevaluate(pTSP: ProblemContextTSP, s: SolutionTSP):
    assert (s.n == pTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pTSP.n-1):
      f += pTSP.dist[s.cities[i]][s.cities[i + 1]];
    f += pTSP.dist[s.cities[int(pTSP.n) - 1]][s.cities[0]];
    return f
import random

def mycallback_constructive(problemCtx: ProblemContextTSP) -> SolutionTSP:
    sol = SolutionTSP()
    for i in range(problemCtx.n):
        sol.cities.append(i)
    random.shuffle(sol.cities)
    sol.n = problemCtx.n
    return sol


# move
class MoveSwap(object):
    def __init__(self):
        #print('__init__ MoveSwap')
        self.i = 0
        self.j = 0

    def __del__(self):
        # print("~MoveSwap")
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_swap(problemCtx: ProblemContextTSP, m: MoveSwap, sol: SolutionTSP) -> MoveSwap:
    i = m.i
    j = m.j
    #
    aux = sol.cities[j]
    sol.cities[j] = sol.cities[i]
    sol.cities[i] = aux
    # must create reverse move (j,i)
    mv = MoveSwap()
    mv.i = j
    mv.j = i
    return mv

# Moves can be applied or not (best performance is to have a True here)
def cba_swap(problemCtx: ProblemContextTSP, m: MoveSwap, sol: SolutionTSP) -> bool:
    return True

# Move equality must be provided
def eq_swap(problemCtx: ProblemContextTSP, m1: MoveSwap, m2: MoveSwap) -> bool:
    return (m1.i == m2.i) and (m1.j == m2.j)

def mycallback_ns_rand_swap(pTSP: ProblemContextTSP, sol: SolutionTSP) -> MoveSwap:
    i = random.randint(0, pTSP.n - 1)
    j = i
    while  j<= i:
        i = random.randint(0, pTSP.n - 1)
        j = random.randint(0, pTSP.n - 1)
    mv = MoveSwap()
    mv.i = i
    mv.j = j
    return mv


# For NSSeq, one must provide a Move Iterator
# A Move Iterator has five actions: Init, First, Next, IsDone and Current


class IteratorSwap(object):
    def __init__(self):
        # print('__init__ IteratorSwap')
        self.k = 0

    def __del__(self):
        # print("__del__ IteratorSwap")
        pass


def mycallback_nsseq_it_init_swap(pTSP: ProblemContextTSP, sol: SolutionTSP) -> IteratorSwap:
    it = IteratorSwap()
    it.i = -1
    it.j = -1
    return it


def mycallback_nsseq_it_first_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    it.i = 0
    it.j = 1


def mycallback_nsseq_it_next_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    if it.j < pTSP.n - 1:
        it.j = it.j+1
    else:
        it.i = it.i + 1
        it.j = it.i + 1

def mycallback_nsseq_it_isdone_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    return it.i >= pTSP.n - 1


def mycallback_nsseq_it_current_swap(pTSP: ProblemContextTSP, it: IteratorSwap):
    mv = MoveSwap()
    mv.i = it.i
    mv.j = it.j
    return mv
# ===========================================
# begins main() python script for TSP ILS/VNS
# ===========================================

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


#####
pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_component) for ILSLevels...")
print("")

pert_idx = pTSP.engine.build_component(
    "OptFrame:ComponentBuilder:ILS:LevelPert:LPlus2",
    "OptFrame:GeneralEvaluator:Evaluator 0  OptFrame:NS 0",
    "OptFrame:ILS:LevelPert")
print("pert_idx=", pert_idx)

pTSP.engine.list_components("OptFrame:")


print("")
print("testing builder (build_single_obj_search) for ILS...")
print("")

sos_idx = pTSP.engine.build_single_obj_search(
    "OptFrame:ComponentBuilder:SingleObjSearch:ILS:ILSLevels",
    "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:LocalSearch 1 OptFrame:ILS:LevelPert 0  10  5")
print("sos_idx=", sos_idx)


print("will start ILS for 3 seconds")

lout = pTSP.engine.run_sos_search(sos_idx, 3.0) # 3.0 seconds max
print('lout=', lout)


print("FINISHED")
