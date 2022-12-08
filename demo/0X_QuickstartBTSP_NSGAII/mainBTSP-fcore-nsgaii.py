# OptFrame Python Demo BTSP - Bi-objective Traveling Salesman Problem

import os

# DO NOT REORDER 'import sys ...'
#import sys
#str_path=os.path.abspath(
#    os.path.join(os.path.dirname(__file__), '../../'))
#sys.path.insert(0, str_path)

# THIS PACKAGE IS LOCAL (../optframe), NOT FROM PACKAGE MANAGER...
# GOOD FOR LOCAL TESTING!

# DO NOT REORDER 'from optframe.engine ...'
#from optframe.engine import Engine

import optframe

class SolutionBTSP(object):
    def __init__(self):
        # number of cities in solution
        self.n = 0
        # visited cities as a list
        self.cities = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionBTSP(n={self.n};cities={self.cities})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo):
        sol2 = SolutionBTSP()
        sol2.n = self.n
        sol2.cities = [i for i in self.cities]
        return sol2

    def __del__(self):
        # print("~SolutionBTSP")
        pass
import math

class ProblemContextBTSP(object):
    def __init__(self):
        print('Init BTSP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of cities
        self.n = 0
        # x coordinates for obj 0
        self.vx0 = []
        # y coordinates for obj 0
        self.vy0 = []
        # distance matrix for obj 0
        self.dist0 = []
        # x coordinates for obj 1
        self.vx1 = []
        # y coordinates for obj 1
        self.vy1 = []
        # distance matrix for obj 1
        self.dist1 = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx0.append(int(id_x_y[1]))
               self.vy0.append(int(id_x_y[2]))
            for i in range(self.n):
               id_x_y = lines[self.n+i+1].split()
               # ignore id_x_y[0]
               self.vx1.append(int(id_x_y[1]))
               self.vy1.append(int(id_x_y[2]))
            #
            self.dist0 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist0[i][j] = round(self.euclidean(self.vx0[i], self.vy0[i], self.vx0[j], self.vy0[j]))
            #
            self.dist1 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist1[i][j] = round(self.euclidean(self.vx1[i], self.vy1[i], self.vx1[j], self.vy1[j]))

    def euclidean(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextBTSP(n={self.n};vx0={self.vx0};vy0={self.vy0};dist0={self.dist0};vx1={self.vx1};vy1={self.vy1};dist1={self.dist1})"

# define two objective functions

def mycallback_fevaluate0(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist0[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist0[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

def mycallback_fevaluate1(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

# THIRD OBJECTIVE
def mycallback_fevaluate2(pBTSP: ProblemContextBTSP, s: SolutionBTSP):
    assert (s.n == pBTSP.n)
    assert (len(s.cities) == s.n)
    # remember this is an API1d method
    f = 0.0
    for i in range(pBTSP.n-1):
      f += pBTSP.dist1[s.cities[i]][s.cities[i + 1]];
    f += pBTSP.dist1[s.cities[int(pBTSP.n) - 1]][s.cities[0]];
    return f

import random

def mycallback_constructive(problemCtx: ProblemContextBTSP) -> SolutionBTSP:
    sol = SolutionBTSP()
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
def apply_swap(problemCtx: ProblemContextBTSP, m: MoveSwap, sol: SolutionBTSP) -> MoveSwap:
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
def cba_swap(problemCtx: ProblemContextBTSP, m: MoveSwap, sol: SolutionBTSP) -> bool:
    return True

# Move equality must be provided
def eq_swap(problemCtx: ProblemContextBTSP, m1: MoveSwap, m2: MoveSwap) -> bool:
    return (m1.i == m2.i) and (m1.j == m2.j)

def mycallback_ns_rand_swap(pBTSP: ProblemContextBTSP, sol: SolutionBTSP) -> MoveSwap:
    i = random.randint(0, pBTSP.n - 1)
    j = i
    while  j<= i:
        i = random.randint(0, pBTSP.n - 1)
        j = random.randint(0, pBTSP.n - 1)
    mv = MoveSwap()
    mv.i = i
    mv.j = j
    return mv


# A Crossover must combine two parent solutions and return two new ones
# Workaround: at this version, this is divided into two callbacks...

from typing import Tuple
from copy import deepcopy

def ox_cross_parts(p1, p2, k1, k2):
    # initialize offspring 's'
    s = deepcopy(p1)
    middle_p1 = p1.cities[k1:k2]
    n = len(p1.cities)
    # create offspring s with the three parts
    s.cities = [-1]*len(p1.cities[:k1]) + middle_p1 + [-1]*len(p1.cities[k2:])
    # list rest of pending elements
    rest = [x for x in p2.cities if x not in middle_p1]
    k=0
    for i in range(0, n):
      if s.cities[i] == -1:
        s.cities[i] = rest[k]
        k = k + 1
    return s

def btsp_ox_crossover(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP ) -> Tuple[SolutionBTSP, SolutionBTSP]:
    assert(pBTSP.n == p1.n)
    assert(p1.n == p2.n)
    assert(pBTSP.n >= 3)
    
    # select cut point
    # NOTE: randint (both sides included)
    k1 = random.randint(1, pBTSP.n - 2)
    k2 = random.randint(k1+1, pBTSP.n - 1)
    #
    s1 = ox_cross_parts(p1, p2, k1, k2)
    s2 = ox_cross_parts(p2, p1, k1, k2)
    #
    return s1, s2

# NOTE: this is just a demo... it has a problem!
# crossover pair may not be fully consistent, as each side can have a different fixed point
# This is a simple workaround for this first version

def mycallback_cross1(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s1

def mycallback_cross2(pBTSP: ProblemContextBTSP, p1: SolutionBTSP, p2: SolutionBTSP) -> SolutionBTSP:
    s1, s2 = btsp_ox_crossover(pBTSP, p1, p2)
    return s2
    
# ============================================
# begins main() python script for BTSP NSGA-II
# ============================================

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
