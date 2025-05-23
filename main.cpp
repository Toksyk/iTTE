// how this is going to work:
// basically, most of the functions and values will be handled in this source file
// those functions will be called from the header, which calls the bindings, which calls this file
// only call the functions with the _c ending in the python files

// do NOT delete the testbind function


#include "lib.h"

void testbind(int x) {
    std::cout << "it works, input: " << x << "\n";
}