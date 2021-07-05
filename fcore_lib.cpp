#include "fcore_lib.h"
//

#include <iostream>

// test if python object is received, plus an int
extern "C" int32_t
fcore_test_1(void* vpython, int32_t sz_vr)
{
   printf("%p | %d\n", vpython, sz_vr);
   return 1;
}

// test if func is received
extern "C" int32_t
fcore_test_func(void* vpython, int32_t (*func)(void*), int32_t sz_vr)
{
   printf("%p | %d\n", vpython, sz_vr);
   printf("%p | func_out= %d | %d\n", vpython, func(vpython), sz_vr);
   return 1;
}
