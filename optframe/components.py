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

class SingleObjSearch(object):
    def __init__(self, _engine: XEngine):
        self.engine = _engine
    def search(self, timelimit: float) -> SearchOutput:
        ...

class LocalSearch(object):
    def __init__(self, _engine: XEngine):
        self.engine = _engine
    # no 'searchFrom' here, yet...
