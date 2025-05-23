// how this is going to work:
// basically, most of the functions and values will be handled in this source file
// those functions will be called from the header, which calls the bindings, which calls this file
// only call the functions with the _c ending in the python files

// do NOT delete the testbind function


#include "lib.h"
#include <vector>
#include <cstring> // For memcpy

void testbind(int x) {
    std::cout << "it works, input: " << x << "\n";
}

void render(const std::vector<std::vector<char>>& game_space) {
    for(size_t col = 0; col < game_space.size(); ++col) {
        for(size_t row = 0; row < game_space[col].size(); ++row) {
            std::cout << game_space[col][row];
        }
        std::cout << "\n";
    }
}

std::vector<std::vector<char>> Init() {
    std::cout << "initializing engine.." << "\n";
    std::vector<std::vector<char>> space { // 11 x 9 grid is the gamespace (editable, its a vector)
        {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'}, // the # is the border. it will be immovable and solid WITH physics properties
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'}
    };
    return space;
}
