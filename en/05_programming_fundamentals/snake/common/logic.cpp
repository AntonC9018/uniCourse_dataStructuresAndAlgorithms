#include "logic.h"

#include <cassert>
#include <iostream>
#include <chrono>

SnakePositionsStorage createSnakePositionStorage(const BoardDimensions& dimensions)
{
    size_t maxSnakeSize = dimensions.totalCells;
    Vector* bodyPositionArray = new Vector[maxSnakeSize];
    std::span<Vector> bodyPositions{ bodyPositionArray, maxSnakeSize };
    return {
        .bodyPositions = bodyPositions,
        .headIndex = 0,
        .snakeLength = 1,
    };
}

void freeSnakePositionStorage(SnakePositionsStorage& snake)
{
    delete[] snake.bodyPositions.data();
}

bool existsSnakeBodyAt(
    const SnakePositionsStorage& snake,
    Vector randomPosition,
    bool includeLast)
{
    size_t lastOffset = snake.snakeLength;
    if (!includeLast)
    {
        lastOffset -= 1;
    }

    for (size_t offset = 0; offset != lastOffset; offset += 1)
    {
        size_t m = snake.bodyPositions.size();
        size_t bodyPartIndex = (snake.headIndex + m - offset) % m;
        Vector snakePosition = snake.bodyPositions[bodyPartIndex];
        if (areVectorsEqual(randomPosition, snakePosition))
        {
            return true;
        }
    }
    return false;
}

static Vector generateRandomPositionForApple(
    const BoardDimensions& dimensions,
    const SnakePositionsStorage& snake,
    RNGState& rngState)
{
    while (true)
    {
        std::uniform_int_distribution<size_t> distribution{ 0, dimensions.totalCells - 1 };
        size_t randomNumber = distribution(rngState);
        size_t col = randomNumber % dimensions.col;
        size_t row = randomNumber / dimensions.col;
        Vector randomPosition{
            .x = static_cast<int>(col),
            .y = static_cast<int>(row),
        };
        
        if (!existsSnakeBodyAt(snake, randomPosition))
        {
            return randomPosition;
        }
    }
}

Direction getNextDirection(
    Direction currentDirection,
    Direction desiredDirection)
{
    Direction oppositeDirection = getOppositeDirection(currentDirection);
    if (oppositeDirection == desiredDirection)
    {
        return currentDirection;
    }
    return desiredDirection;
}

void moveHead(SnakePositionsStorage& snake)
{
    snake.headIndex = (snake.headIndex + 1) % snake.bodyPositions.size();
}

static void adjustCoord(
    int& value, 
    int direction,
    size_t dimension)
{
    ptrdiff_t signedDimension = static_cast<ptrdiff_t>(dimension);
    assert(signedDimension > 0);
    value = static_cast<int>((value + signedDimension + direction) % signedDimension);
}

bool doGameLogic(
    const BoardDimensions& dimensions,
    GameState& state)
{
    Vector headPosition = getHeadPosition(state.snakePositions);
    Vector nextHeadPosition = headPosition;
    const Vector directionAsVector = getDirectionAsVector(state.snakeDirection);
    adjustCoord(nextHeadPosition.x, directionAsVector.x, dimensions.col);
    adjustCoord(nextHeadPosition.y, directionAsVector.y, dimensions.row);

    const bool wasAppleEatenThisTurn = areVectorsEqual(nextHeadPosition, state.applePosition);
    if (wasAppleEatenThisTurn)
    {
        state.snakePositions.snakeLength += 1;
    }
    else if (existsSnakeBodyAt(state.snakePositions, nextHeadPosition, false))
    {
        std::cout << "Game over" << std::endl;
        return true;
    }

    moveHead(state.snakePositions);
    getHeadPosition(state.snakePositions) = nextHeadPosition;

    if (wasAppleEatenThisTurn)
    {
        if (state.snakePositions.snakeLength == dimensions.totalCells)
        {
            std::cout << "You won" << std::endl;
            return true;
        }

        state.applePosition = generateRandomPositionForApple(
            dimensions,
            state.snakePositions,
            state.rngState);
    }

    return false;
}

GameState createInitialGameState(const BoardDimensions& dimensions)
{
    auto snakePositions = createSnakePositionStorage(dimensions);
    Direction snakeDirection = DOWN;

    getHeadPosition(snakePositions) = {
        .x = static_cast<int>(dimensions.col / 2),
        .y = static_cast<int>(dimensions.row / 2),
    };

    RNGState rngState;
    {
        auto time = std::chrono::system_clock::now();
        size_t timeAsNumber = time.time_since_epoch().count();
        rngState.seed(timeAsNumber);
    }

    Vector applePosition = generateRandomPositionForApple(
        dimensions,
        snakePositions,
        rngState);

    return {
        .snakePositions = snakePositions,
        .snakeDirection = snakeDirection,
        .applePosition = applePosition,
        .rngState = rngState,
    };
}

void freeGameState(GameState& state)
{
    freeSnakePositionStorage(state.snakePositions);
}

