#pragma once
#include <cstdlib>

struct Vector
{
    int x;
    int y;
};

struct BoardDimensions
{
    size_t col;
    size_t row;
    size_t totalCells;
};

inline bool areVectorsEqual(Vector a, Vector b)
{
    return a.x == b.x && a.y == b.y;
}

inline BoardDimensions createBoardDimensions(size_t col, size_t row)
{
    return {
        .col = col,
        .row = row,
        .totalCells = col * row,
    };
}

using Direction = int;
static inline const Direction UP = 0;
static inline const Direction RIGHT = 1;
static inline const Direction DOWN = 2;
static inline const Direction LEFT = 3;
static inline const Direction INVALID_DIRECTION = -1;
static inline const int directionCount = 4;

Direction getOppositeDirection(Direction d);
Vector getDirectionAsVector(Direction d);
