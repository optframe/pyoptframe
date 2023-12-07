#!/usr/bin/python3

from typing import Protocol, runtime_checkable, Tuple, Union

# protocols should only depend on 'core'
from optframe.core import SearchOutput

@runtime_checkable
class XSolution(Protocol):
    # this is default, regardless of user implementing it or not...
    def __str__(self) -> str:
        ...

@runtime_checkable
class XProblem(Protocol):
    # this is default, regardless of user implementing it or not...
    def __str__(self) -> str:
        ...

@runtime_checkable
class XIdComponent(Protocol):
    def get_id(self) -> int:
        ...
    def __repr__(self) -> str:
        ...

@runtime_checkable
class XConstructive(Protocol):
    @staticmethod
    def generateSolution(problem: XProblem) -> XSolution:
        ...

@runtime_checkable
class XMaximize(Protocol):
    @staticmethod
    def maximize(problem: XProblem, sol: XSolution) -> float:
        ...

@runtime_checkable
class XMinimize(Protocol):
    @staticmethod
    def minimize(problem: XProblem, sol: XSolution) -> float:
        ...

@runtime_checkable
class XMove(Protocol):
    @staticmethod
    def apply(problemCtx: XProblem, m: 'XMove', sol: XSolution) -> 'XMove':
        ...
    @staticmethod
    def canBeApplied(problemCtx: XProblem, m: 'XMove', sol: XSolution) -> bool:
        ...
    @staticmethod
    def eq(problemCtx: XProblem, m1: 'XMove', m2: 'XMove') -> bool:
        ...

@runtime_checkable
class XNS(Protocol):
    @staticmethod
    def randomMove(problem: XProblem, sol: XSolution) -> XMove:
        ...

@runtime_checkable
class XNSIterator(Protocol):
    @staticmethod
    def first(problemCtx: XProblem, it: 'XNSIterator'):
        ...
    @staticmethod
    def next(problemCtx: XProblem, it: 'XNSIterator'):
        ...
    @staticmethod
    def isDone(problemCtx: XProblem, it: 'XNSIterator') -> bool:
        ...
    @staticmethod
    def current(problemCtx: XProblem, it: 'XNSIterator') -> XMove:
        ...

@runtime_checkable
class XNSSeq(Protocol):
    @staticmethod
    def randomMove(problem: XProblem, sol: XSolution) -> XMove:
        ...
    @staticmethod
    def getIterator(problem: XProblem, sol: XSolution) -> XNSIterator:
        ...

from optframe.core import LibArrayDouble

@runtime_checkable
class XDecoderRandomKeysNoEvaluation(Protocol):
    @staticmethod
    def decodeSolution(p: XProblem, rk : LibArrayDouble) -> XSolution:
        ...

@runtime_checkable
class XDecoderRandomKeysMinimize(Protocol):
    @staticmethod
    def decodeMinimize(p: XProblem, rk : LibArrayDouble, needsSolution: bool) -> Tuple[Union[XSolution,None], float]:
        ...

@runtime_checkable
class XDecoderRandomKeysMaximize(Protocol):
    @staticmethod
    def decodeMaximize(p: XProblem, rk : LibArrayDouble, needsSolution: bool) -> Tuple[Union[XSolution,None], float]:
        ...

@runtime_checkable
class XConstructiveRK(Protocol):
    @staticmethod
    def generateRK(p: XProblem, rk : LibArrayDouble) -> int:
        ...

@runtime_checkable
class XSingleObjSearch(Protocol):
    @staticmethod
    def search(problem: XProblem, sol: XSolution) -> XMove:
        ... 

@runtime_checkable
class XGlobalSearch(Protocol):
    @staticmethod
    def search(problem: XProblem, sol: XSolution) -> XMove:
        ... 

@runtime_checkable
class XEngine(Protocol):
    @staticmethod
    def build_global_search(code: str, args: str) -> int:
        ... 
    @staticmethod
    def run_global_search(g_idx: int, timelimit: float) -> SearchOutput:
        ... 
