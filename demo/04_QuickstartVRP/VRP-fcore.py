# OptFrame Python Demo VRP - Vehicle Routing Problem

import optframe
from typing import List, TypeVar, Dict, Any, Protocol, runtime_checkable #, #Callable
# XSolution = TypeVar('XSolution')

@runtime_checkable
class XSolution(Protocol):
    def __str__(self) -> str:
        ...
    def __deepcopy__(self, memo: Dict[Any, Any]) -> 'XSolution':
        ...

class SolutionVRP(object):
    def __init__(self):
        # list of list ("routes")
        self.sol : List[List[int]] = []
        # ADS: excess per route
        self.ar : List[int] = []

    # MUST provide some printing mechanism
    def __str__(self):
        return f"SolutionVRP(sol={self.sol};ar={self.ar})"

    # MUST provide some deepcopy mechanism
    def __deepcopy__(self, memo : Dict[Any, Any]):
        sol2 = SolutionVRP()
        sol2.sol = [i[:] for i in self.sol]
        sol2.ar  = [i    for i in self.ar]
        return sol2

    def __del__(self):
        # print("~SolutionVRP")
        pass

class ProblemContextVRP(object):
    def __init__(self):
        print('Init VRP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of clients
        self.n = -1
        # number of clients + depot
        #self.N = 0 # n+1
        # delivery packet size for each client
        self.d = []
        # homogeneous capacity among vehicles
        # self.Q = 0
        # x coordinates
        self.vx : List[int] = []
        # y coordinates
        self.vy : List[int] = []
        # distance matrix
        self.dist = []

    def load(self, filename : str):
        # example files
        '''Example: 
            4
            0 10 10
            1 20 40
            2 30 30
            3 40 20
            4 50 50
            10
            4 4 3 3
        '''
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            self.N = self.n+1
            for i in range(self.N):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx.append(int(id_x_y[1]))
               self.vy.append(int(id_x_y[2]))
            #
            self.dist = [[0 for _ in range(self.N)] for _ in range(self.N)]
            for i in range(self.N):
               for j in range(self.N):
                  self.dist[i][j] = round(self.euclidean(self.vx[i], self.vy[i], self.vx[j], self.vy[j]))
            #
            self.Q = int(lines[self.N+1])
            self.d = [int(i) for i in lines[self.N+2].split()]


    def euclidean(self, x1: int, y1: int, x2: int, y2: int) -> float:
        import math
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextVRP(n={self.n};N={self.N};Q={self.Q};d={self.d};vx={self.vx};vy={self.vy};dist={self.dist})"

####### testing #######
# exec(open('VRP-fcore-part2.py').read())
# p = ProblemContextVRP()
# p.load('instance.txt')
# print(p)
# output: ProblemContextVRP(n=4;N=5;Q=10;d=[4, 4, 3, 3];vx=[10, 20, 30, 40, 50];vy=[10, 40, 30, 20, 50];
#         dist=[[0, 32, 28, 32, 57], [32, 0, 14, 28, 32], [28, 14, 0, 14, 28], [32, 28, 14, 0, 32], [57, 32, 28, 32, 0]])
#######################
# full evaluation: count distances (cannot update ADS, since its const)
def fevaluateVRP(pVRP: ProblemContextVRP, s: SolutionVRP):
    # Soma das Distancias
    f = 0.0
    # valor alto para capacidade extra
    W_ExtraCap = 99999.0
    f_extra = 0.0
    for r in range(len(s.sol)):
        # somatorio das demandas na rota
        sumDemands = 0
        for i in range(len(s.sol[r]) - 1):
            f += pVRP.dist[s.sol[r][i]][s.sol[r][i+1]]
            sumDemands += pVRP.d[s.sol[r][i]]
        f += pVRP.dist[s.sol[r][-1]][0]  # retornando ao deposito
        sumDemands += pVRP.d[s.sol[r][-1]]
        if sumDemands > pVRP.Q:
            f_extra += (sumDemands - pVRP.Q)
    return f + W_ExtraCap * f_extra

def frandom(pVRP: ProblemContextVRP) -> SolutionVRP:
    #print(f"frandom(n={pVRP.n})")
    rep = SolutionVRP()

    # mistura todos os clientes (cliente 0 é o 'deposito')
    v = [-1 for _ in range(pVRP.n)]  # informação do contexto
    for i in range(len(v)):
        v[i] = i + 1  # excluindo o deposito 0
    # shuffle (TODO: use randgen)
    import random
    random.shuffle(v)
    #print(v)
    #
    # utilizando a construcao randomica
    # Os clientes são adicionados um por um, a menos que a capacidade seja excedida e uma nova rota seja necessária.
    sumDemands = 9999999  # Acumular demandas na rota atual (começar MUITO GRANDE)
    #
    for i in range(len(v)):
        if sumDemands + pVRP.d[v[i]] > pVRP.Q:
            # começando uma nova rota
            rep.sol.append([0])  # "rota vazia" (deposito 0 está sempre presente)
            sumDemands = 0
        # adicionando um cliente na posicao v[i]
        rep.sol[-1].append(v[i])
        # adicionando as demandas
        sumDemands += pVRP.d[v[i]]
    # rota viável (nao é a melhor)
    return rep

# move
class MoveVRPExchange(object):
    def __init__(self):
        self.r = 0
        self.c1 = 0
        self.c2 = 0

    def __del__(self):
        pass

# Move Apply MUST return an Undo Move or Reverse Move (a Move that can undo current application)
def apply_vrp_exchange(pVRP: ProblemContextVRP, m: MoveVRPExchange, sol: SolutionVRP) -> MoveVRPExchange:
    r = m.r
    c1 = m.c1
    c2 = m.c2
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
def cba_vrp_exchange(pVRP: ProblemContextVRP, m: MoveVRPExchange, sol: SolutionVRP) -> bool:
    rep = getRoutes(sol);  # se.first.getR();
    bool all_positive = (c1 >= 0) && (c2 >= 0) && (r >= 0);
    return all_positive && (rep.at(r).size() >= 2);
    return True

# Move equality must be provided
def eq_vrp_exchange(problemCtx: ProblemContextTSP, m1: MoveSwap, m2: MoveSwap) -> bool:
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
