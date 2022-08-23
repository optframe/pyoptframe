# we need to take care of memory handling... a simple example which is broken
# internal object is lost after function 'test_memory' finishes

def callback_sol_python(sol: FCoreSolution):
    print("sol = ", sol.foo())
    return 1


def test_memory():
    local = FCoreSolution()
    vcpp = fcore_lib.fcore_test_gensolution(local)
    vsol = fcore_lib.fcore_test_invokesolution(
        vcpp, FUNC_TEST(callback_sol_python))
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

# hello
# registering 0x7fa109bf7a00
# will invoke function on internal pointer: 0x7fa109bf7a00
#sol =  30
#vcpp= 15938672
# will invoke function on internal pointer: 0x7fa109bf7a00
# Falha de segmentação (imagem do núcleo gravada)
