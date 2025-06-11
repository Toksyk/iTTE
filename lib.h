#ifndef LIB_H
#define LIB_H
#include <iostream>
#include <vector>
#include <memory>


class Object {
public:
    int x;
    int y;
    char character;

    Object(int x_val, int y_val, char obj_char) : x(x_val), y(y_val), character(obj_char) {
    }
};

// Core

void testbind(int x);
void Init();
void render();
std::unique_ptr<Object> CreateObject(int x, int y, char character);
void AddObject(std::unique_ptr<Object> obj);


extern std::vector<std::vector<char>> game_space;
extern std::vector<std::unique_ptr<Object>> gameObjects;

extern "C" {

    void testbind_c(int x);

    char** Init_c(int* rows, int* cols);

    void render_c(char** game_space_ptr, int rows, int cols);

    void AddObject_c(int x, int y, char character);

    void MoveObject_c(int object_index, int new_x, int new_y);

    char GetInput_c(); // DEPRECATED ; FOR WINDOWS ONLY

    void endscene_c(char** game_space_ptr, int rows);
}

#endif // LIB_H
