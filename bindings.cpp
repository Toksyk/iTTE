#include "lib.h"

extern "C" {
    void testbind_c(int x) {
        testbind(x);
    }
}