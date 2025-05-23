#include "lib.h"
#include <vector>
#include <cstring> // for memcpy

extern "C" {
    void testbind_c(int x) {
        testbind(x);
    }

    // reallocate the silly vector and remake the pointers
    char** Init_c(int* row, int* col) {
        std::vector<std::vector<char>> game_space_vec = Init();

        *row = game_space_vec.size();
        if (*row == 0) { // memory leak prevention at its finest
            *col = 0;
            return nullptr;
        }
        *col = game_space_vec[0].size();

        char** game_space_ptr = new char*[*row];
        for (int i = 0; i < *row; ++i) {
            game_space_ptr[i] = new char[*col];
            memcpy(game_space_ptr[i], game_space_vec[i].data(), *col * sizeof(char));
        }
        return game_space_ptr;
    };

    void render_c(char** game_space_ptr, int row, int col) {
        // new std::vector<std::vector<char>> from the pointers
        std::vector<std::vector<char>> game_space_vec(row, std::vector<char>(col));
        for (int i = 0; i < row; ++i) {
            for (int j = 0; j < col; ++j) {
                game_space_vec[i][j] = game_space_ptr[i][j];
            }
        }
        render(game_space_vec);
    };

    void endscene_c(char** game_space_ptr, int row) {
        if (game_space_ptr) {
            for (int i = 0; i < row; ++i) {
                delete[] game_space_ptr[i];
            }
            delete[] game_space_ptr;
        }
    }
}
