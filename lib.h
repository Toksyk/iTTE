#ifndef LIB_H
#define LIB_H
#include <iostream>

void testbind(int x);

extern "C" {
    void testbind_c(int x);
}
#endif