#ifndef fcore_LIB_H
#define fcore_LIB_H

#include <cstdint> // int32_t
#include <stdio.h>

// test if python object is received, plus an int
extern "C" int32_t
fcore_test_1(void* vpython, int32_t sz_vr);

// test if func is received
extern "C" int32_t
fcore_test_func(void* vpython, int32_t (*func)(void*), int32_t sz_vr);

#endif // fcore_LIB_H
