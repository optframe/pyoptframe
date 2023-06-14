#!/usr/bin/python3

from optframe.protocols import *

##### Id

class IdUnknown(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdUnknown("+str(self.id)+")"
    
class IdNone(object):
    def get_id(self):
        return -1
    def __repr__(self) -> str:
        return "IdNone"

class IdConstructive(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdConstructive("+str(self.id)+")"
    
class IdInitialSearch(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdInitialSearch("+str(self.id)+")"
    
class IdGeneralEvaluator(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdGeneralEvaluator("+str(self.id)+")"
    
class IdEvaluator(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdEvaluator("+str(self.id)+")"
    
class IdListEvaluator(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdListEvaluator("+str(self.id)+")"
    
class IdNS(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdNS("+str(self.id)+")"
    
class IdNSSeq(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdNSSeq("+str(self.id)+")"
    
class IdListNS(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdListNS("+str(self.id)+")"
    
class IdListNSSeq(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdListNSSeq("+str(self.id)+")"
    
class IdDecoderRandomKeysNoEvaluation(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdDecoderRandomKeysNoEvaluation("+str(self.id)+")"

class IdConstructiveRK(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdConstructiveRK("+str(self.id)+")"

class IdDecoderRandomKeys(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdDecoderRandomKeys("+str(self.id)+")"

class IdInitialEPopulationRK(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdInitialEPopulationRK("+str(self.id)+")"
    
    
############

class IdGlobalSearch(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdGlobalSearch("+str(self.id)+")"
    
class IdSingleObjSearch(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdSingleObjSearch("+str(self.id)+")"
    
class IdLocalSearch(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdLocalSearch("+str(self.id)+")"
    
class IdListLocalSearch(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdListLocalSearch("+str(self.id)+")"
    
class IdILSLevelPert(object):
    def __init__(self, id: int):
        self.id = id
    def get_id(self):
        return self.id
    def __repr__(self) -> str:
        return "IdILSLevelPert("+str(self.id)+")"

#############

class Move(object):
    def __str__(self) -> str:
        ...
    def apply(self, problemCtx: XProblem, sol: XSolution) -> 'Move':
        ...
    def canBeApplied(self, problemCtx: XProblem, sol: XSolution) -> bool:
        return True
    def eq(self, problemCtx: XProblem, m2: 'Move') -> bool:
        ...

class NSIterator(object):
    def first(self, p: XProblem):
        ...
    def next(self, p: XProblem):
        ...
    def isDone(self, p: XProblem) -> bool:
        ...
    def current(self, p: XProblem) -> Move:
        ...

# there is no NS component, only XNS protocol
# there is no NSSeq component, only XNSSeq protocol

##############



#############

class SingleObjSearch(object):
    def __init__(self, _engine: XEngine):
        self.engine = _engine
    def search(self, timelimit: float) -> SearchOutput:
        ...

class LocalSearch(object):
    def __init__(self, _engine: XEngine):
        self.engine = _engine
    # no 'searchFrom' here, yet...
