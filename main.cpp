// how this is going to work:
// basically, most of the functions and values will be handled in this source file
// those functions will be called from the header, which calls the bindings, which calls this file
// only call the functions with the _c ending in the python files

// do NOT delete the testbind function


#include "lib.h"
#include <vector>
#include <memory>  // For smart pointers (std::unique_ptr)
#include <iostream>


void testbind(int x) {
    std::cout << "it works, input: " << x << "\n";
}

std::vector<std::unique_ptr<Object>> gameObjects; // make this a class if the engine makes it big (hell yeah)

std::vector<std::vector<char>> game_space;


void render() { // no longer needs args
    std::vector<std::vector<char>> current_frame_space = game_space;
    for (const auto& obj_ptr : gameObjects) {
        // check if in bounds
        if (obj_ptr->y >= 0 && obj_ptr->y < current_frame_space.size() &&
            obj_ptr->x >= 0 && obj_ptr->x < current_frame_space[obj_ptr->y].size()) {
            current_frame_space[obj_ptr->y][obj_ptr->x] = obj_ptr->character;
        }
    }
    // now do rows first
    for (size_t row = 0; row < current_frame_space.size(); ++row) {
        for (size_t col = 0; col < current_frame_space[row].size(); ++col) {
            std::cout << current_frame_space[row][col];
        }
        std::cout << "\n";
    }
}

void Init() { // no longer returns space
    std::cout << "initializing engine.." << "\n";
    // The '#' characters represent borders, and ' ' represents empty space
    game_space = {
        {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
        {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'}
    };
}

std::unique_ptr<Object> CreateObject(int x, int y, char character) {
    return std::make_unique<Object>(x, y, character);
}

void AddObject(std::unique_ptr<Object> obj) {
    if (obj) {
        gameObjects.push_back(std::move(obj)); // GOD BLESS STD::MOVE !!! RAAAAAHHHHHHHH
    }
}



// for the future of this engine: stop parsing gamespace. it will add a lot of technical debt but parsing it so much is just so
// bad for optimisation purposes. just make it a variable in here and dont parse it at all to the python file. it doesnt need it.

// ^^^ now finished in this file, now change bindings.py :333
