#ifndef LIB_H
#define LIB_H
#include <iostream>
#include <vector>

void testbind(int x);

std::vector<std::vector<char>> Init();

void render(const std::vector<std::vector<char>>& game_space); // const important i think

extern "C" {
    void testbind_c(int x);

    // cant send full vector, so send the size (the pointer was already passed)
    char** Init_c(int* rows, int* cols);
    void render_c(char** game_space_ptr, int rows, int cols);
    void endscene_c(char** game_space_ptr, int rows); // Function to free the memory

}
#endif
