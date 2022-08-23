# this is fixed because of Py_IncRef...
# However! We would likely need to DecRef this at some moment in the future.


def test_memory():
    a = ExampleSol()
    #
    a.n = 11
    b1, b2 = copy(a), deepcopy(a)
    #
    a.n = 12
    a.bag.append(5)
    #
    print('a:', a.n, a.bag)
    print('b1:', b1.n, b1.bag)
    print('b2:', b2.n, b2.bag)
    #
    pyo = ctypes.py_object(a)
    ctypes.pythonapi.Py_IncRef(pyo)  # will give reference to fcore_lib
    #
    vcpp = fcore_lib.fcore_test_gensolution(pyo)
    vsol = fcore_lib.fcore_test_invokesolution(
        vcpp, FUNC_TEST(callback_sol_python))

    # ctypes.pythonapi.Py_IncRef(vsol)
    return vcpp


# =============================
#       BEGIN SCRIPT
# =============================
print("hello")

vcpp = test_memory()
print("vcpp=", vcpp)
vsol = fcore_lib.fcore_test_invokesolution(
    vcpp, FUNC_TEST(callback_sol_python))
print("vsol=", vsol)
