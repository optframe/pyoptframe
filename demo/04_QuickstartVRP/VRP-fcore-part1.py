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