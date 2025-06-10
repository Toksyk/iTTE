#include "lib.h"
#include <vector>
#include <cstring>  // For memcpy
#include <cstdio>   // For getchar()
#include <memory> 

//TODO:
// * will need to make function to change the character of an object, for now not needed

extern std::vector<std::vector<char>> global_base_game_space;

extern std::vector<std::unique_ptr<Object>> gameObjects;

extern "C" { // wrappers

    void testbind_c(int x) {
        testbind(x);
    }

    char** Init_c(int* row, int* col) {
        Init();

        *row = global_base_game_space.size(); // this all below wont be used after bindings.py wont require the game state
        if (*row == 0) {
            *col = 0;
            return nullptr;
        }
        *col = global_base_game_space[0].size();

        char** game_space_ptr = new char*[*row];
        for (int i = 0; i < *row; ++i) {
            game_space_ptr[i] = new char[*col];
            memcpy(game_space_ptr[i], global_base_game_space[i].data(), *col * sizeof(char));
        }
        return game_space_ptr;
    }

    // accepts args from bindings.py (game_space_ptr) for compatibility
    // ignored for now, soon to be deleted
    void render_c(char** game_space_ptr, int row, int col) {
        render();
    }

    void AddObject_c(int x, int y, char character) {
        AddObject(CreateObject(x, y, character));
    }

    // add and create now together

    void MoveObject_c(int object_index, int new_x, int new_y) {
        if (object_index >= 0 && object_index < gameObjects.size()) {
            gameObjects[object_index]->x = new_x;
            gameObjects[object_index]->y = new_y;
        } else {
            std::cerr << "Error: cant move object to: " << object_index << "\n";
        }
    }

    char GetInput_c() { // DEPRECATED
        // FOUND WINDOWS SPECIFIC METHOD OF NOT WAITING FOR ENTER, MIGHT BE A BAD CASE
        return static_cast<char>(getchar());
    }

    // this will need to be remade after bindings.py gets updated
    void endscene_c(char** game_space_ptr, int row) {
        if (game_space_ptr) {
            for (int i = 0; i < row; ++i) {
                delete[] game_space_ptr[i];
            }
            delete[] game_space_ptr;
        }

        gameObjects.clear();
    }
}
