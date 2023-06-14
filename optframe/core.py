#!/usr/bin/python3

import ctypes 
import sys
from copy import deepcopy
from enum import Enum, IntEnum

# ===================================
# no 'optframe.' import allowed here!
# ===================================

class SearchStatus(Enum):
    NO_REPORT = 0x00
    FAILED = 0x01
    RUNNING = 0x02
    # RESERVED = 0x04
    IMPOSSIBLE = 0x08
    NO_SOLUTION = 0x10
    IMPROVEMENT = 0x20
    LOCAL_OPT = 0x40
    GLOBAL_OPT = 0x80

class SearchOutput(ctypes.Structure):
    _fields_ = [("status", ctypes.c_int),  # optframe.SearchStatus
                ("has_best", ctypes.c_bool),
                ("best_s", ctypes.py_object),
                ("best_e", ctypes.c_double)]

    def __str__(self):
        return f"SearchOutput(status={self.status};has_best={self.has_best};best_s={self.best_s};best_e={self.best_e};)"


class LibArrayDouble(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),  
                ("v", ctypes.POINTER(ctypes.c_double))]

    def __str__(self):
        return f"LibArrayDouble(size={self.size};v={self.v};)"

# optframe.LogLevel
class LogLevel(IntEnum):
    Silent = 0
    Error = 1
    Warning = 2
    Info = 3
    Debug = 4
# example:
# if (loglevel >= LogLevel::Warning) { ... }


class CheckCommandFailCode(IntEnum):
    CMERR_EV_BETTERTHAN = 2001
    CMERR_EV_BETTEREQUALS = 2002
    CMERR_MOVE_EQUALS = 3001
    CMERR_MOVE_HASREVERSE = 3002
    CMERR_MOVE_REVREV_VALUE = 3004
    CMERR_MOVE_REVSIMPLE = 3005
    CMERR_MOVE_REVFASTER = 3006
    CMERR_MOVE_REALREVFASTER = 3008
    CMERR_MOVE_COST = 3007


# ==============================
#       HELPER FUNCTIONS
# ==============================

# def callback_utils_incref(pyo: ctypes.py_object):
#    # print("callback_utils_incref: ", sys.getrefcount(pyo), " will get +1")
#    ctypes.pythonapi.Py_IncRef(pyo)
#    return sys.getrefcount(pyo)

def callback_utils_decref(pyo):
    if (isinstance(pyo, ctypes.py_object)):
        pyo = pyo.value
        print("pyo:", pyo)
    # print("callback_utils_decref: ", sys.getrefcount(pyo), " will get -1")
    # IMPORTANT: 'pyo' may come as a Real Python Object, not a 'ctypes.py_object'
    cast_pyo = ctypes.py_object(pyo)
    #
    ctypes.pythonapi.Py_DecRef(cast_pyo)
    x = sys.getrefcount(pyo)
    return x


def callback_sol_tostring(sol, pt: ctypes.c_char_p, ptsize: ctypes.c_size_t):
    mystr = sol.__str__()
    mystr_bytes = mystr.encode()
    pa = ctypes.cast(pt, ctypes.POINTER(ctypes.c_char * ptsize))
    pa.contents.value = mystr_bytes
    return len(mystr)


def callback_sol_deepcopy_utils(sol):
    # print("invoking 'callback_sol_deepcopy'... sol=", sol)
    if (isinstance(sol, ctypes.py_object)):
        # this should never happen!
        assert (False)
    sol2 = deepcopy(sol)
    return sol2

# ==============================
