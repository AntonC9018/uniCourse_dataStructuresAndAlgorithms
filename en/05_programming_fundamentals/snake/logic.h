#pragma once

#include <random>
#include <span>
#include "common.h"

struct SnakePositionsStorage
{
    std::span<Vector> bodyPositions;
    size_t headIndex;
    size_t snakeLength;
};

using RNGState = std::mt19937;

SnakePositionsStorage createSnakePositionStorage(const BoardDimensions& dimensions);
void freeSnakePositionStorage(SnakePositionsStorage& snake);

bool existsSnakeBodyAt(
    const SnakePositionsStorage& snake,
    Vector randomPosition,
    bool includeLast = true);

Direction getNextDirection(
    Direction currentDirection,
    Direction desiredDirection);

inline Vector& getHeadPosition(SnakePositionsStorage& snake)
{
    return snake.bodyPositions[snake.headIndex];
}

void moveHead(SnakePositionsStorage& snake);

struct GameState
{
    SnakePositionsStorage snakePositions;
    Direction snakeDirection;
    Vector applePosition;
    RNGState rngState;
};

bool doGameLogic(
    const BoardDimensions& dimensions,
    GameState& state);
GameState createInitialGameState(const BoardDimensions& dimensions);
void freeGameState(GameState& state);
