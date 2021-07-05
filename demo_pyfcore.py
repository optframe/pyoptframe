#!/usr/bin/python3

import ctypes
from ctypes import *
#
#from functools import total_ordering
from typing import TypeVar, Type
#T = TypeVar('T', bound='BigInteger')

fcore_lib = ctypes.cdll.LoadLibrary('build/fcore_lib.so')
fcore_lib.fcore_test_1.argtypes = [
    # ctypes.c_void_p, ctypes.c_int]
    ctypes.py_object, ctypes.c_int]
fcore_lib.fcore_test_1.restype = ctypes.c_bool

# function evaluate(int[] v, int sz) -> int (evaluation)
FUNC_EVALUATE = CFUNCTYPE(c_int, POINTER(c_int), c_int)
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.py_object))
#
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.c_void_p))
#
#FUNC_TEST = CFUNCTYPE(c_int, POINTER(ctypes.py_object))
FUNC_TEST = CFUNCTYPE(c_int, ctypes.py_object)
fcore_lib.fcore_test_func.argtypes = [
    # ctypes.c_void_p, FUNC_TEST, ctypes.c_int]
    ctypes.py_object, FUNC_TEST, ctypes.c_int]
fcore_lib.fcore_test_func.restype = ctypes.c_bool

# ===============
# VERY GOOD EXAMPLE IN PYTHON
# https://stackoverflow.com/questions/52053434/how-to-cast-a-ctypes-pointer-to-an-instance-of-a-python-class#52055019
#
# ===================


# class FCore(object):
class FCore(object):
    # def __init__(self, param=0):
    #    self.p = param
    def foo(self):
        return 30  # self.p


def callback(userData: FCore):
    print("From Python: {:s}".format(callback.__name__))
    print(type(userData))

    return userData.foo()


#x = [10]
x = FCore()
print(x.foo())
print(type(x))
#p_x = ctypes.cast(ctypes.py_object(x), ctypes.c_void_p)
# print(type(p_x))

fcore_lib.fcore_test_1(x, 50)

print("")
print("calling 'fcore_test_func'")
fcore_lib.fcore_test_func(x, FUNC_TEST(callback), 50)

#fcore_lib.fcore_test_1(p_x, 50)

# function evaluate(int[] v, int sz) -> int (evaluation)
#FUNC_EVALUATE = CFUNCTYPE(c_int, POINTER(c_int), c_int)

# https://stackoverflow.com/questions/50889988/the-attribute-of-ctypes-py-object
# ctypes.py_object ..

print("bye")

exit(0)
